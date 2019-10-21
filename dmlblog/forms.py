from django import forms
# from django.views.generic import ListView  # , DetailView
from .models import Post  # , Comment
from pagedown.widgets import PagedownWidget

# from django.db.models.query import QuerySet


class PostForm(forms.ModelForm):
    # template="path/to/template.html", css=("custom/css1.css", "custom/css2.css"))
    text = forms.CharField(widget=PagedownWidget())
    published_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = (
            "title",
            "text",
            "tags",
            "video",
            "image",
            "image_width",
            "image_height",
            "draft",
            "published_date",
        )


"""
class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class TagIndexView(TagMixin, ListView):
    paginate_by = 5  # "5"

    def get_queryset(self) -> "QuerySet[Post]":
        return Post.objects.filter(tags__slug=self.kwargs.get("pk"))
"""