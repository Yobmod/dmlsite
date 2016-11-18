from django import forms
from django.views.generic import DetailView, ListView
from .models import Post, Comment


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text', "tags", "video", "image", "image_width", "image_height", "slug")
		
		
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('author', 'text',)
		queryset = Post.objects.all()
		

class TagMixin(object):
	def get_context_data(self, **kwargs):
		context = super(TagMixin, self).get_context_data(**kwargs)
		context["tags"] = Tag.objects.all()
		return context
		
class TagIndexView(TagMixin, ListView):
	paginate_by = "5"
	def get_queryset(self):
		return Post.objects.filter(tags__slug=self.kwargs.get(pk))
