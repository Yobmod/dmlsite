from django.contrib import admin
from .models import Comment
from .forms import CommentForm


admin.site.register(Comment)
