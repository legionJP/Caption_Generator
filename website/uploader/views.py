from django.shortcuts import render
#from django.http import HttpResponse
#from django.template.loader import get_template


# Create your views here.

#def index(request):
    #return HttpResponse("Hello  upload your video here for the captions ")

def home(request):
    # template = get_template('uploader/home.html')
    # print(template.origin)
    return render(request,'uploader/home.html')
#-------------------------------------------------------------------

from django.shortcuts import render, redirect
from .models import videos
from .forms import VideoForm
from .tasks import extract_subtitles

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            extract_subtitles.delay(video.id)
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, 'home.html', {'form': form})

def video_list(request):
    video = videos.objects.all()
    return render(request, 'home.html', {'videos': video})


# #------------------------------------------------------------------------------
# Here’s the updated home.html file:

# HTML

# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Video Uploader</title>
# </head>
# <body>
#     <h1>Upload Video</h1>
#     <form method="post" enctype="multipart/form-data">
#         {% csrf_token %}
#         {{ form.as_p }}
#         <button type="submit">Upload</button>
#     </form>

#     <h1>Video List</h1>
#     <ul>
#         {% for video in videos %}
#         <li>{{ video.title }} - Processed: {{ video.processed_status }}</li>
#         {% endfor %}
#     </ul>

#     {% if video %}
#     <video controls>
#         <source src="{{ video.video_file.url }}" type="video/mp4">
#         {% for lang, subtitle in video.subtitles.items %}
#         <track src="{{ subtitle }}" kind="subtitles" srclang="{{ lang }}" label="{{ lang }}">
#         {% endfor %}
#     </video>
#     {% endif %}
# </body>
# </html>
# AI-generated code. Review and use carefully. More info on FAQ.
# Adjustments to Your Views
# Make sure your views are correctly passing the form and the list of videos to the template:

# Python

# from django.shortcuts import render, redirect
# from .models import videos
# from .forms import VideoForm
# from .tasks import extract_subtitles

# def home(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             video = form.save()
#             extract_subtitles.delay(video.id)
#             return redirect('home')
#     else:
#         form = VideoForm()
    
#     video_list = videos.objects.all()
#     return render(request, 'uploader/home.html', {'form': form, 'videos': video_list})
# AI-generated code. Review and use carefully. More info on FAQ.
# Ensure Your Form Handles File Uploads
# Make sure your VideoForm is set up to handle file uploads:

# Python

# from django import forms
# from .models import videos

# class VideoForm(forms.ModelForm):
#     class Meta:
#         model = videos
#         fields = ['video_file', 'title']
# AI-generated code. Review and use carefully. More info on FAQ.
# Model Adjustments
# Ensure your videos model is set up to store the video file and any other necessary fields:

# Python

# from django.db import models

# class videos(models.Model):
#     title = models.CharField(max_length=100)
#     video_file = models.FileField(upload_to='videos/')
#     processed_status = models.BooleanField(default=False)
# AI-generated code. Review and use carefully. Mo