from django import forms
from django.views.generic import DetailView, ListView
from .models import Post, Comment


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text', "tags",)
		
		
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('author', 'text',)
		queryset = Post.objects.all()
		

		

			

		
	
		
		

		
		