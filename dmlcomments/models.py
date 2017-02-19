from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from dmlblog.models import Post

class Comment(models.Model):
	#post = models.ForeignKey('dmlblog.Post', related_name='commentsapp')
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True) #rmv null/blank for new db
	object_id = models.PositiveIntegerField(null=True, blank=True) #rmv null/blank for new db
	content_object = GenericForeignKey('content_type', 'object_id')
	author = models.ForeignKey('auth.User')
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	approved_comment = models.BooleanField(default=False)

	def approve(self):
		self.approved_comment = True
		self.save()

	def __str__(self):
		return self.text

	def approved_comments(self):
		return self.comments.filter(approved_comment=True)
