from .models import video
from django import forms


class VideoForm(forms.ModelForm):
    
    class Meta:
        model=video
        fields =['title','url','youtube_id']
