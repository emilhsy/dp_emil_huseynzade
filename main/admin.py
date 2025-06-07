from django.contrib import admin
from .models import Post, Comment

# Register models to make them editable in the Django admin panel
admin.site.register(Post)
admin.site.register(Comment)