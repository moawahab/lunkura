from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default="Coding")


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('home')


class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=225)
    slug = models.SlugField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=225, default="coding")

    def __str__(self):
        return self.title + '|' + str(self.author)  
    
    def get_absolute_url(self):
        return reverse('home')