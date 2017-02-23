from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class CommentManager(models.Manager):
	def all(self):
		qs = super(CommentManager, self).filter(parent=None)
		return qs

	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		qs = super(CommentManager, self).filter(content_type=content_type, object_id=instance.id).filter(parent=None)
		return qs


class Comment(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True) #rmv null/blank for new db
	object_id = models.PositiveIntegerField(null=True, blank=True) #rmv null/blank for new db
	content_object = GenericForeignKey('content_type', 'object_id')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
	visitor = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	approved_comment = models.BooleanField(default=False)
	parent = models.ForeignKey('Comment', null=True, blank=True)

	objects = CommentManager()

	class Meta:
		ordering = ['created_date']

	def __str__(self):
		return self.text

	def children(self):
		return Comment.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True

	def approve(self):
		self.approved_comment = True
		self.save()

	def approved_comments(self):
		return self.comments.filter(approved_comment=True)
