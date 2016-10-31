from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Choice, Question


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

# def make_poll(request)
	# pub = datetime.datetime.now()
	# Question.question_text = input("What is your poll question")
	# Question.save()
	# return Httprespon("Derp")
