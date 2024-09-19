from django.urls import path
from . import views

urlpatterns= [
    path("", views.home,name="uplopader-home"),
    path('home/',views.home, name='uploader-home'),
    path('search/', views.search, name='uploader-search')
   # path('video/<int:video_id>/', views.video_player, name='video_player'),
    # path('home/',views.upload_video, name='uploader-home'),
    # path('home/',views.video_list,name='uploader-home')

]