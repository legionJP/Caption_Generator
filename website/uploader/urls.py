from django.urls import path
from . import views

urlpatterns= [
    path("", views.home,name="uplopader-home"),
    path('home/',views.home, name='uploader-home'),
]