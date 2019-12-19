from django.contrib import admin
from .models import Post, Rating, Theme

# Register your models here.

admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(Theme)