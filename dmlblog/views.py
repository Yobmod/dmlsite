from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .utils import get_read_time
from .models import Post, Comment
from .forms import PostForm, CommentForm, TagIndexView, TagMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
#from dmlcomments.models import Comment
#from dmlcomments.forms import CommentForm
try:
    from urllib.parse import quote_plus
except:
    pass

def post_list(request):
	posts = Post.objects.filter(draft=False).filter(published_date__lte=timezone.now()).order_by('published_date').reverse()

	query = request.GET.get("q")
	if query:
		posts = posts.filter(Q(title__icontains=query)|
							Q(author__username__icontains=query)|
							Q(author__first_name__icontains=query)|
							Q(author__last_name__icontains=query)|
							Q(text__icontains=query)).distinct()
	paginator = Paginator(posts, 5)
	page_request_var = "post_page"
	page = request.GET.get(page_request_var)
	#print(paginator.count)
	#print(paginator.num_pages)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)#if not enough, give first page
	except(EmptyPage or InvalidPage):
		queryset = paginator.page(paginator.num_pages)#if too many, give last page
	context = {'posts':posts,
						'page_request_var': page_request_var,
						'obj_list':queryset,}
	return render(request, 'dmlblog/post_list.html', context)

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	share_string = quote_plus(post.text)
	comments = post.comments
	form = CommentForm()
	context = {
		"post": post,
		"share_string": share_string,
		"comments": comments,
		"form":form,
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
	return render(request, 'dmlblog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST or None, request.FILES or None, instance=post)
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
