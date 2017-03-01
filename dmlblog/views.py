from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib import messages
from .utils import get_read_time
from .models import Post
from .forms import PostForm, TagIndexView, TagMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from dmlcomments.models import Comment
from dmlcomments.forms import CommentForm
try:
	from urllib.parse import quote_plus
except:
	pass

def post_test(request):
	pass

def post_list(request):
	posts = Post.objects.filter(draft=False).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
	c_type = ContentType.objects.get_for_model(Post)
	post_id = posts.values_list('id')
	post_comments = Comment.objects.filter(content_type=c_type, object_id__in=post_id)
	query = request.GET.get("q")
	if query:
		posts = posts.filter(Q(title__icontains=query) |
							 Q(author__username__icontains=query) |
							 Q(author__first_name__icontains=query) |
							 Q(author__last_name__icontains=query) |
							 Q(text__icontains=query)).distinct()
	paginator = Paginator(posts, 5)
	page_request_var = "post_page"
	page = request.GET.get(page_request_var)
	# print(paginator.count)
	# print(paginator.num_pages)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)  # if not enough, give first page
	except(EmptyPage or InvalidPage):
		# if too many, give last page
		queryset = paginator.page(paginator.num_pages)
	context = {'posts': posts,
			   'post_comments': post_comments,
			   'page_request_var': page_request_var,
			   'obj_list': queryset, }
	return render(request, 'dmlblog/post_list.html', context)


def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	share_string = quote_plus(post.text)
	# comments = post.comments #FK changed to GFK
	#form = CommentForm()
	comments = Comment.objects.filter_by_instance(post)
	initial_data = {"content_type": post.get_content_type,
					"object_id": post.id,
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
			author=request.user,
			content_type=content_type,
			object_id=obj_id,
			text=content_data,
			parent=parent_obj,			)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
	context = {
		"post": post,
		"share_string": share_string,
		"comments": comments,
		"form": form,
	}
	return render(request, 'dmlblog/post_detail.html', context)


@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			if post.draft:
				messages.success(request, "New draft created!")
			else:
				messages.success(request, "New post created!")
				return redirect('blog:post_detail', pk=post.pk)
		else:
			messages.error(request, "New post failed!")
	else:
		form = PostForm()
	context = {'form': form}
	return render(request, 'dmlblog/post_edit.html', context)


@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST or None,
						request.FILES or None, instance=post)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			form.save_m2m()
			messages.success(request, "Post updated")
			return redirect('blog:post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'dmlblog/post_edit.html', {'form': form})


@login_required
def post_unpublish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.unpublish()
	messages.success(request, "Post unpublished to drafts")
	return redirect('blog:post_list')


@login_required
def post_draft_list(request):
	drafts = Post.objects.filter(draft=True).order_by('created_date')
	return render(request, 'dmlblog/post_draft_list.html', {'drafts': drafts})


@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('blog:post_detail', pk=post.pk)


@login_required
def draft_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	messages.success(request, "Draft deleted")
	return redirect('blog:post_draft_list')


def add_comment_to_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('blog:post_detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'dmlblog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('dmlblog.views.post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	post_pk = comment.post.pk
	comment.delete()
	return redirect('dmlblog.views.post_detail', pk=post_pk)


def tag_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return redirect('dmlblog.views.post_detail', pk=post.pk)
