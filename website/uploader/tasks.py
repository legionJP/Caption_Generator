from celery import shared_task
import subprocess
from .models import videos, Subtitle
from google.cloud import speech_v1p1beta1 as speech
#from google.cloud.speech_v1p1beta1 import enums ,types

@shared_task
def extract_subtitles(video_id):
    video = videos.objects.get(id=video_id)
    video_path = video.v_file.path
    output_path = f"{video_path}.srt"

    # Run CCExtractor to extract subtitles
    command = f"ccextractor {video_path} -o {output_path}"
    subprocess.run(command, shell=True)

    # Read the extracted subtitles and save them to the database
    with open(output_path, 'r') as file:
        for line in file:
            if '-->' in line:
                timestamps = line.strip().split(' --> ')
                start_time = timestamps[0]
                end_time = timestamps[1]
                content = next(file).strip()
                Subtitle.objects.create(video=video, language='en', content=content, start_time=start_time, end_time=end_time)

    video.processed_status = True
    video.save()

#-----------------------------------------------------------------------------------------#

@shared_task
def generate_subtitles(video_id):
    video = videos.objects.get(id=video_id)
    video_path = video.v_file.path

    client = speech.SpeechClient()
    with open(video_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='en-US',
        enable_word_time_offsets=True
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            start_time = word_info.start_time.total_seconds()
            end_time = word_info.end_time.total_seconds()
            content = word_info.word
            Subtitle.objects.create(video=video, language='en', content=content, start_time=start_time,end_time=end_time)

    video.processed_status = True
    video.save()

@shared_task
def process_video(video_id):
    try:
        generate_subtitles(video_id)
    except Exception as e:
        print(f"Subtitle generation failed: {e}")
        extract_subtitles(video_id)
