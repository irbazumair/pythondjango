from django.contrib import admin
from .models import Category, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'published_on']  # Fixed commas

admin.site.register(Category)
admin.site.register(Post, PostAdmin)