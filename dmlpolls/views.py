from django.shortcuts import get_object_or_404, render  # , redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
# from django.contrib.auth.decorators import login_required
from .forms import AddPollForm, ChoiceForm
from .models import Choice, Question  # , Opinion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dmlcomments.models import Comment
from dmlcomments.forms import CommentForm
from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from typing import Optional, cast


def poll_list(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    # queryset_list = Question.objects.all()
    c_type = ContentType.objects.get_for_model(Question)
    # post_id = posts.values_list('id')
    poll_comments = Comment.objects.filter(content_type=c_type)
    counts = 1
    for question in questions:
        for comment in poll_comments:
            if comment.content_object and comment.content_object.id == question.id:
                counts += 1
                question.poll_comments.count = counts
    query = request.GET.get("q")
    if query:
        questions = questions.filter(Q(question_text__icontains=query) |
                                     Q(author__username__icontains=query) |
                                     Q(author__first_name__icontains=query) |
                                     Q(author__last_name__icontains=query)).distinct()
    paginator = Paginator(questions, 5)
    page_request_var = "polls_page"
    page = request.GET.get(page_request_var)
    try:
        if isinstance(page, (str, int)):
            page_set = paginator.page(page)
        else:
            raise TypeError
    except (PageNotAnInteger, TypeError):  # if not enough, give first page
        page_set = paginator.page(1)
    except EmptyPage:  # if too many, give last page
        page_int = paginator.num_pages
        page_set = paginator.page(page_int)
    context = {'questions': questions, 'page_request_var': page_request_var, 'obj_list': page_set}
    return render(request, 'dmlpolls/poll_list.html', context)


def poll_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=pk)
    comments = question.comments
    counts = 1
    for comment in comments:
        if comment.content_object and comment.content_object.id == question.id:
            counts += 1
            question.poll_comments.count = counts
    initial_data = {"content_type": question.get_content_type,
                    "object_id": question.id,
                    "author_id": request.user}

    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        content_type_str: str = form.cleaned_data.get("content_type")
        content_type_model = content_type_str.split()[-1]
        content_type = ContentType.objects.get(model=content_type_model)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("text")
        parent_obj = None
        try:
            parent_id: Optional[int] = int(cast(str, request.POST.get("parent_id")))
        except Exception:
            parent_id = None

        if parent_id is not None:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            author=request.user,
            content_type=content_type,
            object_id=obj_id,
            text=content_data,
            parent=parent_obj,			)
        if new_comment.content_object:
            return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    context = {"form": form, 'question': question, "comments": comments, }
    return render(request, 'dmlpolls/poll_detail.html', context)


class IndexView(generic.ListView):
    template_name = 'dmlpolls/poll_index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self) -> QuerySet:
        """    Return the last five published questions (not including those set to be
        published in the future).    """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'dmlpolls/poll_detail.html'

    def get_queryset(self) -> 'QuerySet[Question]':
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'dmlpolls/poll_results.html'

    def get_queryset(self) -> 'QuerySet[Question]':
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


def addpoll(request: HttpRequest) -> HttpResponse:
    form = AddPollForm(request.POST or None)
    if form.is_valid():  # on submit
        poll = form.save(commit=False)
        poll.author = request.user
        poll.save()
        # question_text = form.cleaned_data.get('question_text')
        # questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

        # return render(request, 'dmlpolls/poll_list.html', {'questions': questions})
        return poll_list(request)
        # context ={'form':form}
        # return render(request, 'dmlpolls/add_choice.html', context)
    else:  # on first load
        form = AddPollForm()
        context = {'form': form}
        return render(request, 'dmlpolls/add_poll.html', context)


def add_choice(request: HttpRequest, question_id: int) -> HttpResponse:
    question = Question.objects.get(pk=question_id)
    form = ChoiceForm(request.POST)
    if form.is_valid():
        form.save(commit=False)
        # addpoll.question = question
        # addpoll.vote = 0
        # addpoll.question.save()
        return render(request, 'dmlpolls/poll_detail.html', {'question': question})
        # return HttpResponse('gbhbetg')
    else:
        form = ChoiceForm()
        return render(request, 'dmlpolls/add_choice.html', {'form': form, 'question_id': question_id, })


def vote(request: HttpRequest, pk: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'dmlpolls/poll_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a user hits the Back button.
        return HttpResponseRedirect(reverse('dmlpolls:poll_results', args=[question.id]))
        # return HttpResponse("placeholder for votes number %s." % question_id)


def results(request: HttpRequest, pk: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'dmlpolls/poll_results.html', {'question': question})
