from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import AddPollForm, ChoiceForm
from .models import Choice, Question, Opinion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def poll_list(request):
	questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
	#queryset_list = Question.objects.all()
	query = request.GET.get("q")
	if query:
		questions = questions.filter(Q(question_text__icontains=query)|
									Q(author__username__icontains=query)|
									Q(author__first_name__icontains=query)|
									Q(author__last_name__icontains=query)).distinct()
	paginator = Paginator(questions, 5)
	page_request_var = "polls_page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)#if not enough, give first page
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)#if too many, give last page
	context = {'questions': questions, 'page_request_var': page_request_var, 'obj_list':queryset }
	return render(request, 'dmlpolls/poll_list.html', context)


def poll_detail(request, pk):
	question = get_object_or_404(Post, pk=question_id)
	return render(request, 'dmlpolls/detail.html', {'question': question})

class IndexView(generic.ListView):
	template_name = 'dmlpolls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""    Return the last five published questions (not including those set to be
		published in the future).    """
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'dmlpolls/detail.html'

	def get_queryset(self):
		"""Excludes any questions that aren't published yet."""
		return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'dmlpolls/results.html'

	def get_queryset(self):
		"""Excludes any questions that aren't published yet."""
		return Question.objects.filter(pub_date__lte=timezone.now())

def addpoll(request):
	form = AddPollForm(request.POST or None)
	if form.is_valid():
		poll = form.save(commit=False)
		poll.author = request.user
		poll.save()
		question_text = form.cleaned_data.get('question_text')
		questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
		return render(request, 'dmlpolls/poll_list.html', {'questions': questions})
		#context ={'form':form}
		#return render(request, 'dmlpolls/add_choice.html', context)
	else:
		form = AddPollForm()
		context ={'form':form}
		return render(request, 'dmlpolls/add_poll.html', context)

def add_choice(request, question_id):
	question = Question.objects.get(pk = question_id)
	form = ChoiceForm(request.POST)
	if form.is_valid():
		poll = form.save(commit = False)
		#addpoll.question = question
		#addpoll.vote = 0
		#addpoll.question.save()
		form.save()
		#return render(request, 'dmlpolls/detail.html', {'question': question})
		return HttpResponse('gbhbetg')
	else:
		form = ChoiceForm()
		return render(request,'dmlpolls/add_choice.html', {'form': form, 'question_id': question_id,})



def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#Redisplay the question voting form.
		return render(request, 'dmlpolls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a user hits the Back button.
		return HttpResponseRedirect(reverse('poll_results', args=(question.id,)))
		#return HttpResponse("placeholder for votes number %s." % question_id)
