from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
	author = models.ForeignKey('auth.user', null=True)
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)
	end_date = models.DateTimeField(blank=True,null=True)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=7) <= self.pub_date <= now
		was_published_recently.admin_order_field = 'pub_date'
		was_published_recently.boolean = True
		was_published_recently.short_description = 'Published recently?'
		poll_author.admin_order_field = 'author'

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text

class Opinion(models.Model):
	question = models.ForeignKey(Question)
	choice_vote = models.ForeignKey(Choice)
