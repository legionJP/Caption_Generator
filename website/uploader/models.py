from django.db import models

# Create your models here.

class videos(models.Model):
    title= models.CharField(max_length=255)
    v_file=models.FileField(upload_to='/videos') #stored in the videos/ directory within the media root.
    uploaded_at= models.DateTimeField(auto_now_add=True)
    processed_status= models.BooleanField(default=False)
    subtitles = models.JSONField(null=True,blank=True)

    def __str__(self):
     return self.title
    
#------------------------------------------------------------------------------
class Subtitle(models.Model):
   video= models.ForeignKey(videos,related_name='subtitles',on_delete=models.CASCADE)
   language= models.CharField(max_length=10)
   content = models.TextField()
   timestamp = models.FloatField()

   def __str__(self):
      return f"{self.videos.title} - {self.language} - {self.timestamp}"
    
    