from django.shortcuts import render, redirect,get_object_or_404
from .models import videos
from .forms import VideoForm
from .tasks import generate_subtitles #extract_subtitles,
from django.http import HttpResponseRedirect
from django.urls import reverse

# def home(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             video = form.save()
#             generate_subtitles.delay(video.id)
#             return HttpResponseRedirect(reverse('uploader-home')) #render(request,'home.html')
#     else:
#         form = VideoForm()
    
#     video_list = videos.objects.all()
#     return render(request, 'uploader/home.html', {'form': form, 'videos': video_list})


def home(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            generate_subtitles.delay(video.id)
            return HttpResponseRedirect(reverse('uploader-home'))
    else:
        form = VideoForm()
    
    video_list = videos.objects.all()
    return render(request, 'uploader/home.html', {'form': form, 'videos': video_list})





# def upload_video(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST, request.FILES)
#         if form.is_valid():
#             video = form.save()
#             extract_subtitles.delay(video.id)
#             return redirect('video_list')
#     else:
#         form = VideoForm()
#     return render(request, 'home.html', {'form': form})

# def video_list(request):
#     video = videos.objects.all()
#     return render(request, 'home.html', {'videos': video})