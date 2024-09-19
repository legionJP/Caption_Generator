# Docker Setup for Django Application

##  Make the file with the below name in root directory of the project  
- Docker
- Docker Compose

## Project Structure
myproject/ │ ├── Dockerfile ├── docker-compose.yml ├── requirements.txt ├── manage.py ├── myproject/ │ ├── init.py │ ├── settings.py │ ├── urls.py │ ├── wsgi.py │ ├── celery.py │ ├── uploader/ │ ├── init.py │ ├── admin.py │ ├── apps.py │ ├── forms.py │ ├── models.py │ ├── tasks.py │ ├── views.py │ ├── urls.py │ ├── templates/ │ │ └── blog_app/ │ │ └── search.html │ │ └── home.html │ ├── migrations/ │ │ └── init.py │ └── static/



## Step 1: Create `requirements.txt` like below
- command  pip freeze > requirements.txt

```
Django>=3.2,<4.0
psycopg2-binary>=2.8
celery>=5.0
kombu>=5.0
whisper
ffmpeg-python
```
## Step 2: Create Dockerfile

## Step 3: Create docker-compose.yml

## Step 4: Update settings.py for Postgres SQL if not setup

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'db',
        'PORT': 5432,
    }
}

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'


```

## Step 5: Build and Run Docker Containers

```
docker-compose build
docker-compose up
docker-compose run web python manage.py migrate
```

# Step 6: Access Your Application
- Visit http://localhost:8000.