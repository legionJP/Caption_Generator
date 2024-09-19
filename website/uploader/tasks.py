from celery import shared_task
import subprocess
from .models import videos, Subtitle
import os
import ffmpeg
import whisper
import shlex
from django.conf import settings
#-----------------------------------------------------------------------------------------#
from celery import shared_task
import subprocess
from .models import videos, Subtitle
import os
import ffmpeg
import whisper
import shlex
from django.conf import settings

# Helper function to convert seconds to SRT time format (hh:mm:ss,ms)
def convert_seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Helper function to extract captions using ffmpeg
def extract_captions_with_ffmpeg(video_path, output_srt_path):
    try:
        command = f'ffmpeg -i "{video_path}" -map 0:s:0 "{output_srt_path}"'
        subprocess.run(shlex.split(command), check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting captions with ffmpeg: {e}")
        return False

@shared_task
def generate_subtitles(video_id):
    try:
        video = videos.objects.get(id=video_id)
        video_path = video.v_file.path
        video.processed_status = True
        video.save()

        # Define languages to generate subtitles for
        languages = ['en', 'hi', 'fr']
        
        subtitles_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
        os.makedirs(subtitles_dir, exist_ok=True)

        # Load the Whisper model (this can be 'tiny', 'base', 'small', 'medium', or 'large')
        model = whisper.load_model("base")


        for lang in languages:
            result = model.transcribe(video_path, language=lang)

            # Create the path to save the .srt subtitle file
            subtitle_srt_path = os.path.join(subtitles_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}_{lang}.srt")

            # Save the Whisper-generated subtitles in .srt format
            with open(subtitle_srt_path, 'w', encoding='utf-8') as file:
                for i, segment in enumerate(result['segments'], 1):
                    start_time = segment['start']
                    end_time = segment['end']
                    text = segment['text']

                    # Convert start_time and end_time to SRT format
                    start_time_srt = convert_seconds_to_srt_time(start_time)
                    end_time_srt = convert_seconds_to_srt_time(end_time)

                    file.write(f"{i}\n{start_time_srt} --> {end_time_srt}\n{text}\n\n")

            # Extract captions from the video using ffmpeg
            extracted_srt_path = os.path.join(subtitles_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}_captions.srt")
            if extract_captions_with_ffmpeg(video_path, extracted_srt_path):
                print(f"Captions extracted and saved at {extracted_srt_path}")

            # Save .srt subtitle to the database
            relative_path_srt = os.path.relpath(subtitle_srt_path, settings.MEDIA_ROOT)
            Subtitle.objects.create(
                video=video,
                language=lang,
                file=relative_path_srt
            )

        print(f"Subtitles generated and embedded successfully for video ID {video_id}")

    except Exception as e:
        print(f"Subtitle generation failed for video ID {video_id}: {e}")
