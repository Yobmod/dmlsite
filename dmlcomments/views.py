from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from dmlcomments.models import Comment
from dmlcomments.forms import CommentForm

def comment_thread(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	content_object = comment.content_object #gets poll/post the comment is from
	content_id = comment.content_object.id
	initial_data ={"content_type": comment.content_type,
				   "object_id": comment.object_id,
				   "author_id": request.user}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("text")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()
		new_comment, created = Comment.objects.get_or_create(
							author = request.user,
							content_type= content_type,
							object_id = obj_id,
							text = content_data,
							parent = parent_obj,			)
		return HttpResponseRedirect(comment.get_absolute_url())
	context = {'comment': comment, 'form': form}
	return render(request, 'comment_thread.html', context)
