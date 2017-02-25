from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from dmlcomments.models import Comment
from dmlcomments.forms import CommentForm

def comment_thread(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	context = {'comment': comment}
	return render(request, 'comment_thread.html', context)
