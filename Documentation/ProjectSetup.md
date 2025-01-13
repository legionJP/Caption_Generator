# Video Caption Generator 

#
# Project  Requirements Description: 

## Website Features and Requirements

## Features

1. **Video Upload and Processing**: Develop a website that allows users to upload videos, which will be processed in the background. After processing and extracting subtitles from the video, the subtitles should be returned to the frontend, integrated with the video, and displayed as closed captions. Ensure that the logic supports multiple language subtitles.

2. **Search Functionality**: Implement a search feature on the website that enables users to search for a phrase within the video and retrieve the timestamp of its occurrence. When a user clicks on the timestamp, the video should start playing from that specific point. Ensure that the search functionality is case-insensitive.

3. **List View for Uploaded Videos**: Implement a list view for uploaded video files. When a video file is selected, it should retrieve the corresponding video and subtitles, and provide all the aforementioned features.

### Requirements

1. **Subtitle Extraction**: Utilize `ffmpeg` for extracting subtitles from videos. The use of any other service for subtitle extraction is not permitted. Download `ffmpeg` from [here](https://www.ffmpeg.org/download.html).
2. **Docker**: Containerize the entire application, including the Django backend, PostgreSQL database, and any other services, using Docker. Provide a `docker-compose.yml` file to facilitate easy setup of the development environment.
3. **Backend**: Develop the backend using Django.
4. **Frontend**: The UI (frontend) of the website will not be a criterion for judgment. Therefore, a simple and functional frontend is acceptable. Evaluation will be based solely on the use of Django and PostgreSQL.
5. **Storage**: Store the processed videos in the Django media folder and save the extracted subtitles in a PostgreSQL database.
6. **Test Case**: The web application should successfully process and handle the provided sample video.
