from django.db import models

# Create your models here.
from django.db import models
class Section(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
class Reply(models.Model):
    content = models.TextField()
    reply_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='images')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True, related_name='images')
    image_path = models.CharField(max_length=500)