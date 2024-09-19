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


#----------------------Search View--------------------------#
from django.db.models import Q
from .models import videos, Subtitle

def search(request):
    results = []
    query = request.POST.get('query', '').lower()
    context = {
        'results': results,
        'query_title': 'All Results',
        'query': query
    }

    if query:
        subtitles = Subtitle.objects.filter(content__icontains=query)
        for subtitle in subtitles:
            video = subtitle.video
            results.append({
                'video_title': video.title,
                'timestamp': subtitle.start_time,
                'video_url': video.v_file.url
            })
        context['results'] = results
        context['query_title'] = f'Search results for "{query}"'
    else:
        context['query_title'] = "No search query entered"

    return render(request, 'uploader/home.html', context)


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