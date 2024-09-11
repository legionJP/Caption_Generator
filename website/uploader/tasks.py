from celery import shared_task
import subprocess
from .models import videos, Subtitle

@shared_task
def extract_subtitles(video_id):
    video = videos.objects.get(id=video_id)
    video_path = video.video_file.path
    output_path = f"{video_path}.srt"

    # Run ccextractor to extract subtitles
    command = f"ccextractor {video_path} -o {output_path}"
    subprocess.run(command, shell=True)

    # Read the extracted subtitles and save them to the database
    with open(output_path, 'r') as file:
        for line in file:
            # Parse the subtitle file and save each subtitle with its timestamp
            # This is a simplified example; you may need to adjust the parsing logic
            if '-->' in line:
                timestamp = line.strip()
                content = next(file).strip()
                Subtitle.objects.create(video=video, language='en', content=content, timestamp=timestamp)

    video.processed = True
    video.save()
