from django import forms
from .models import videos

class VideoForm(forms.ModelForm):
    class Meta:
        model = videos
        fields = ['title', 'v_file']
