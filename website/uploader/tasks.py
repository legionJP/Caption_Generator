from celery import shared_task
import subprocess
from .models import videos, Subtitle
import os
import ffmpeg
import whisper
#from google.cloud.speech_v1p1beta1 import enums ,types

#-----------------------------------------------------------------------------------------#

# @shared_task
# def generate_subtitles(video_id):
#     video = videos.objects.get(id=video_id)
#     video_path = video.v_file.path

#     client = speech.SpeechClient()
#     with open(video_path, 'rb') as audio_file:
#         content = audio_file.read()

#     audio = speech.RecognitionAudio(content=content)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         language_code='en-US',
#         enable_word_time_offsets=True
#     )

#     response = client.recognize(config=config, audio=audio)

#     for result in response.results:
#         alternative = result.alternatives[0]
#         for word_info in alternative.words:
#             start_time = word_info.start_time.total_seconds()
#             end_time = word_info.end_time.total_seconds()
#             content = word_info.word
#             Subtitle.objects.create(video=video, language='en', content=content, start_time=start_time,end_time=end_time)

#     video.processed_status = True
#     video.save()

# #------------------------------------------------------------------
# @shared_task
# def extract_subtitles(video_id):
#     video = videos.objects.get(id=video_id)
#     video_path = video.v_file.path
#     output_path = f"{video_path}.srt"

#     # Run CCExtractor to extract subtitles
#     command = f"ccextractor {video_path} -o {output_path}"
#     subprocess.run(command, shell=True)

#     # Read the extracted subtitles and save them to the database
#     with open(output_path, 'r') as file:
#         for line in file:
#             if '-->' in line:
#                 timestamps = line.strip().split(' --> ')
#                 start_time = timestamps[0]
#                 end_time = timestamps[1]
#                 content = next(file).strip()
#                 Subtitle.objects.create(video=video, language='en', content=content, start_time=start_time, end_time=end_time)

#     video.processed_status = True
#     video.save()
# #====

# @shared_task
# def process_video(video_id):
#     try:
#         generate_subtitles(video_id)
#     except Exception as e:
#         print(f"Subtitle generation failed: {e}")
#         extract_subtitles(video_id)


#------------------------------------------code2---------------------------------------------#

# @shared_task
# def generate_subtitles(video_id):
#     try:
#         video = videos.objects.get(id=video_id)
#         video_path = video.v_file.path
#         audio_path = f"{video_path}.wav"
#         whisper_output_path = f"{video_path}_whisper.srt"
#         ccextractor_output_path = f"{video_path}_ccextractor.srt"

#         # Extract audio using ffmpeg
#         ffmpeg.input(video_path).output(audio_path).run()

#         # Load Whisper model
#         model = whisper.load_model("base")

#         # Transcribe audio to text using Whisper
#         result = model.transcribe(audio_path)

#         # Save the Whisper-generated subtitles
#         with open(whisper_output_path, 'w') as file:
#             for segment in result['segments']:
#                 start_time = segment['start']
#                 end_time = segment['end']
#                 text = segment['text']
#                 file.write(f"{start_time} --> {end_time}\n{text}\n\n")

#         # Extract existing subtitles using CCExtractor
#         command = f"ccextractor {video_path} -o {ccextractor_output_path}"
#         subprocess.run(command, shell=True)

#         # Read and save Whisper-generated subtitles to the database
#         for segment in result['segments']:
#             start_time = segment['start']
#             end_time = segment['end']
#             text = segment['text']
#             Subtitle.objects.create(video=video, language='en', content=text, start_time=start_time, end_time=end_time)

#         # Read and save CCExtractor-generated subtitles to the database
#         with open(ccextractor_output_path, 'r') as file:
#             for line in file:
#                 if '-->' in line:
#                     timestamps = line.strip().split(' --> ')
#                     start_time = timestamps[0]
#                     end_time = timestamps[1]
#                     content = next(file).strip()
#                     Subtitle.objects.create(video=video, language='en', content=content, start_time=start_time, end_time=end_time)

#         video.processed_status = True
#         video.save()
#         print(f"Subtitles generated successfully for video ID {video_id}")

#     except Exception as e:
#         print(f"Subtitle generation failed for video ID {video_id}: {e}")


#----------------------------------code3-----------------------------------------------


from celery import shared_task
import subprocess
from .models import videos, Subtitle
import os
import ffmpeg
import whisper


@shared_task
def generate_subtitles(video_id):
    try:
        video = videos.objects.get(id=video_id)
        video_path = video.v_file.path
        audio_path = f"{video_path}.wav"
        whisper_output_path = f"{video_path}_whisper.srt"
        embedded_video_path = f"{video_path}"
        ccextractor_output_path = f"{video_path}_ccextractor.srt"

        # Extract audio using ffmpeg
        ffmpeg.input(video_path).output(audio_path).run()

        # Load Whisper model
        model = whisper.load_model("base")

        # Transcribe audio to text using Whisper
        result = model.transcribe(audio_path)

        # Save the Whisper-generated subtitles
        with open(whisper_output_path, 'w') as file:
            for segment in result['segments']:
                start_time = segment['start']
                end_time = segment['end']
                text = segment['text']
                file.write(f"{start_time} --> {end_time}\n{text}\n\n")

        # Embed subtitles into the video using FFmpeg
        command = f"ffmpeg -i {video_path} -vf subtitles={whisper_output_path} {embedded_video_path}"
        subprocess.run(command, shell=True)

        # Extract existing subtitles using CCExtractor
        command = f"ccextractor {embedded_video_path} -o {ccextractor_output_path}"
        subprocess.run(command, shell=True)

        # Save Whisper-generated subtitles to the database
        for segment in result['segments']:
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text']
            Subtitle.objects.create(video=video, language='en', content=text, start_time=start_time, end_time=end_time)

        # Save CCExtractor-generated subtitles to the database
        if os.path.exists(ccextractor_output_path):
            with open(ccextractor_output_path, 'r') as file:
                for line in file:
                    if '-->' in line:
                        timestamps = line.strip().split(' --> ')
                        start_time = timestamps[0]
                        end_time = timestamps[1]
                        content = next(file).strip()
                        Subtitle.objects.create(video=video, language='en', content=content, start_time=start_time, end_time=end_time)

        video.processed_status = True
        video.save()
        print(f"Subtitles generated and embedded successfully for video ID {video_id}")

    except Exception as e:
        print(f"Subtitle generation failed for video ID {video_id}: {e}")
