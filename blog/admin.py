from django.contrib import admin

# Register your models here.
from .models import Post, Category
# Minimal registration of Models.
admin.site.register(Post)
admin.site.register(Category)