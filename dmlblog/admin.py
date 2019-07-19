from django.contrib import admin
from .models import Post  # , Comment
from .forms import PostForm


class PostAdmin(admin.ModelAdmin):
    list_display = ["__str__", "author", "created_date", "published_date"]
    form = PostForm

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
# admin.site.register(Comment)
