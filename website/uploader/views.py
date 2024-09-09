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