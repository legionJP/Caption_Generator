# Setting up the django project and app 

1. `run the command to start the django project after python3 installation, and venv activation`

``` 
django-admin startproject 'project_name' 
python manage.py runserver
```

2. `create the app inside the your project withiin the same directory`

```
python manage.py startapp 'appname'

```
3. `First we have to create the DB  to make migrations here we are using the Postgre SQL`

[1.] Install the PostgreSQL on your system and then PostgreSQL Adapter for python 
[2.] Than make the migration for the database

```
1. Install PostgreSQL and Dependencies (on linux system)
sudo apt install postgresql postgresql-contrib libpq-dev python3-dev

2. Install psycopg2
pip install psycopg2

3. Create a PostgreSQL Database and User, so Log into PostgreSQL
sudo -u postgres psql

4. Create a new database and user:

CREATE DATABASE mydatabase;
CREATE USER myuser WITH PASSWORD 'mypassword';

5. Grant the user access to the database:

GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

6. logout
\q

7. Update the database in settings.py , use the PostgreSQL engine and username, password , host, and port
```
4.  `Apply Migrations Run the following commands it also create the necessary database tables:`

```
python manage.py makemigrations
python manage.py migrate
```

# Django Developer Assignment

We at Fatmug are looking for a candidate to help develop, maintain, and optimize our backend infrastructure to scale and manage our product as we grow exponentially.

## Assignment

1. **Video Upload and Processing**: Develop a website that allows users to upload videos, which will be processed in the background. After processing and extracting subtitles from the video, the subtitles should be returned to the frontend, integrated with the video, and displayed as closed captions. Ensure that the logic supports multiple language subtitles.

2. **Search Functionality**: Implement a search feature on the website that enables users to search for a phrase within the video and retrieve the timestamp of its occurrence. When a user clicks on the timestamp, the video should start playing from that specific point. Ensure that the search functionality is case-insensitive.

3. **List View for Uploaded Videos**: Implement a list view for uploaded video files. When a video file is selected, it should retrieve the corresponding video and subtitles, and provide all the aforementioned features.

### Requirements

1. **Subtitle Extraction**: Utilize `ccextractor` for extracting subtitles from videos. The use of any other service for subtitle extraction is not permitted.
2. **Docker**: Containerize the entire application, including the Django backend, PostgreSQL database, and any other services, using Docker. Provide a `docker-compose.yml` file to facilitate easy setup of the development environment.
3. **Backend**: Develop the backend using Django.
4. **Frontend**: The UI (frontend) of the website will not be a criterion for judgment. Therefore, a simple and functional frontend is acceptable. Evaluation will be based solely on the use of Django and PostgreSQL.
5. **Storage**: Store the processed videos in the Django media folder and save the extracted subtitles in a PostgreSQL database.
6. **Test Case**: The web application should successfully process and handle the provided sample video.

### Submission

- Include a `screenshots` folder in the project directory containing screenshots of the application in use. Capture screenshots of every possible action.
- Upload the project to GitHub and provide the repository link.