from celery import shared_task
import subprocess
from .models import videos, Subtitle
import os
import ffmpeg
import whisper
import shlex
from django.conf import settings
#from google.cloud.speech_v1p1beta1 import enums ,types

#-----------------------------------------------------------------------------------------#


@shared_task
def generate_subtitles(video_id):
    
    try:
        video = videos.objects.get(id=video_id)
        video_path = video.v_file.path
# -----------------------for generating the subtitles directly with the uploaded video---------------


        # Load Whisper model
        model = whisper.load_model("base")

        # Define languages to generate subtitles for
        #languages = ['en', 'es', 'fr', 'de','']  # English, Spanish, French, German
        languages = ['en', 'hi', 'fr', 'de'] 
           # 'es', 'it', 'pt', 'ru', 'ja', 'ko', 'zh',
            #'ar', 'bn', 'pl', 'vi', 'tr', 'nl', 'he', 'el']
            # Add more supported language codes if necessary
        
        subtitles_dir = os.path.join(settings.MEDIA_ROOT, 'subtitles')
        os.makedirs(subtitles_dir, exist_ok=True)

        for lang in languages:
            result = model.transcribe(video_path, language=lang)

               # Create the path to save the .srt subtitle file in 'subtitles/' directory
            subtitle_srt_path = os.path.join(subtitles_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}_{lang}.srt")


            # Save the Whisper-generated subtitles in .srt format
            #subtitle_path = f"{os.path.splitext(video_path)[0]}_{lang}.srt"
            with open(subtitle_srt_path, 'w') as file:
                for i, segment in enumerate(result['segments'], 1):
                    start_time = segment['start']
                    end_time = segment['end']
                    text = segment['text']

                    # Convert start_time and end_time to SRT format
                    start_time_srt = convert_seconds_to_srt_time(start_time)
                    end_time_srt = convert_seconds_to_srt_time(end_time)

                    file.write(f"{i}\n{start_time_srt} --> {end_time_srt}\n{text}\n\n")
             

                # Convert .srt to .vtt after generating the .srt file
            # subtitle_vtt_path = os.path.join(subtitles_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}_{lang}.vtt") 
            # convert_srt_to_vtt(subtitle_srt_path, subtitle_vtt_path) 
            # Save subtitle to database
             # Save the relative path to the database
            relative_path = os.path.relpath(subtitle_srt_path, settings.MEDIA_ROOT) #(subtitle_srt_path, settings.MEDIA_ROOT)
            Subtitle.objects.create(
                video=video,
                language=lang,
                file=relative_path #os.path.relpath(subtitle_path, settings.MEDIA_ROOT)
            )
    


        # audio_path = f"{os.path.splitext(video_path)[0]}.mp3"  # Save audio as .mp3
        # whisper_output_path = f"{os.path.splitext(video_path)[0]}_whisper.srt"
        # embedded_video_path = f"{os.path.splitext(video_path)[0]}_with_subs.mp4"

        # # Step 1: Extract audio using ffmpeg
        # ffmpeg.input(video_path).output(audio_path).run()

        # # Step 2: Load Whisper model
        # model = whisper.load_model("base")

        # # Step 3: Transcribe audio to text using Whisper
        # result = model.transcribe(audio_path)

        # # Step 4: Save the Whisper-generated subtitles in SRT format
        # with open(whisper_output_path, 'w') as file:
        #     for i, segment in enumerate(result['segments'], 1):
        #         start_time = segment['start']
        #         end_time = segment['end']
        #         text = segment['text']
                
        #         # Convert start_time and end_time to SRT format (hh:mm:ss,milliseconds)
        #         start_time_srt = convert_seconds_to_srt_time(start_time)
        #         end_time_srt = convert_seconds_to_srt_time(end_time)
                
        #         file.write(f"{i}\n{start_time_srt} --> {end_time_srt}\n{text}\n\n")

        # # Step 5: Check if subtitle file exists
        # if not os.path.exists(whisper_output_path):
        #     raise FileNotFoundError(f"Subtitle file not found: {whisper_output_path}")

        # # Step 6: Embed subtitles into the video using FFmpeg
        # command = f"ffmpeg -i {shlex.quote(video_path)} -vf subtitles={shlex.quote(whisper_output_path)} -c:v libx264 {shlex.quote(embedded_video_path)}"
        # print(f"Running command: {command}")
        # result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # print(result.stdout)
        # print(result.stderr)

        # if result.returncode != 0:
        #     raise RuntimeError(f"ffmpeg command failed: {result.stderr}")

        # # Step 7: Save Whisper-generated subtitles to the database
        # for segment in result['segments']:
        #     start_time = segment['start']
        #     end_time = segment['end']
        #     text = segment['text']
        #     Subtitle.objects.create(video=video, language='en', content=text, start_time=start_time, end_time=end_time)

        # Step 8: Mark video as processed
        video.processed_status = True
        video.save()
        print(f"Subtitles generated and embedded successfully for video ID {video_id}")

    except Exception as e:
        print(f"Subtitle generation failed for video ID {video_id}: {e}")

# Helper function to convert seconds to SRT time format (hh:mm:ss,ms)
def convert_seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


# # SRT to VTT conversion function
# def convert_srt_to_vtt(srt_path, vtt_path):
#     with open(srt_path, 'r') as srt_file:
#         srt_content = srt_file.read()

#     # Replace commas in SRT timestamps with dots for VTT format, and add WEBVTT header
#     vtt_content = 'WEBVTT\n\n' + srt_content.replace(',', '.')

#     with open(vtt_path, 'w') as vtt_file:
#         vtt_file.write(vtt_content)

#     print(f"Converted {srt_path} to {vtt_path}")

