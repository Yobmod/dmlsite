from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
# from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from dmlcomments.models import Comment
from dmlcomments.forms import CommentForm
from dmlblog.models import Post
from dmlpolls.models import Question


def comment_thread(request: HttpRequest, pk: int) -> HttpResponse:
    # comment = get_object_or_404(Comment, pk=pk)
    try:
        comment = Comment.myobjects.get_by_pk(pk)
    except Exception:
        raise Http404
    if not comment.is_parent:
        comment = comment.parent  # if comment is not a parent, find parent instead
    # content_object = comment.content_object  # gets poll/post the comment is from
    # content_id = content_object.id
    initial_data = {
        "content_type": comment.content_type,
        "object_id": comment.object_id,
        "author_id": request.user,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("text")
        parent_obj = None
        parent_id_str = request.POST.get("parent_id")
        if parent_id_str:
            parent_id = int(parent_id_str)
        else:
            parent_id = 0
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            author=request.user,
            content_type=content_type,
            object_id=obj_id,
            text=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(comment.get_absolute_url())
    context = {"comment": comment, "form": form}
    return render(request, "comment_thread.html", context)


@login_required  # redirects them to login page if not loggedin
def comment_delete(request: WSGIRequest, pk: int) -> HttpResponse:
    # comment = get_object_or_404(Comment, pk=pk)
    try:
        comment = Comment.objects.get(pk=pk)
    except Exception:
        raise Http404
    if comment.author != request.user and request.user.is_staff is False: 
        response = HttpResponse("You do not have delete permissions")
        response.status_code = 403
        return response  # only let the author delete. Rediirect to "not allowed page"

    # content_object = comment.content_object #gets poll/post the comment is from
    # content_id = comment.content_object.id
    if request.method == "POST":
        # if not comment.is_parent:  #only delete replies. If parent, replace with "Deleted"
        assert comment.content_object
        parent_obj_url = comment.content_object.get_absolute_url()
        comment.delete()
        messages.success(request, "Comment was deleted")
        return HttpResponseRedirect(parent_obj_url)
    context = {"comment": comment}
    return render(request, "confirm_delete.html", context)


@login_required
def comment_approve(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    assert comment.content_object
    return redirect("dmlblog.views.post_detail", pk=comment.content_object.id)


@login_required
def comment_remove(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    if isinstance(comment.content_object, Post):
        post_pk = comment.content_object.id
        return redirect("dmlblog.views.post_detail", pk=post_pk)
    elif isinstance(comment.content_object, Question):
        Q_pk = comment.content_object.id
        return redirect("dmlblog.views.poll_detail", pk=Q_pk)
    else:
        raise Http404("ohoh")
