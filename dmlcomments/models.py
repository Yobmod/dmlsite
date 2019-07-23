from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone

from django.db.models import QuerySet
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from dmlblog.models import Post
    from dmlpolls.models import Question


class CommentManager(models.Manager):
    def all(self) -> 'QuerySet[Comment]':
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance: Union['Post', 'Question']) -> 'QuerySet[Comment]':
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = (
            super(CommentManager, self)
            .filter(content_type=content_type, object_id=obj_id)
            .filter(parent=None)
        )
        return qs


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey("content_type", "object_id")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    visitor = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)

    objects = CommentManager()

    class Meta:
        ordering = ["created_date"]

    def __str__(self) -> str:
        return self.text

    def get_absolute_url(self) -> str:
        return reverse("comments:comment_thread", kwargs={"pk": self.pk})

    def get_delete_url(self) -> str:
        return reverse("comments:comment_delete", kwargs={"pk": self.pk})

    def children(self) -> "QuerySet[Comment]":
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self) -> bool:
        if self.parent is not None:
            return False
        return True

    def approve(self) -> None:
        self.approved_comment = True
        self.save()

    def approved_comments(self) -> 'QuerySet[Comment]':
        qs: 'QuerySet[Comment]' = self.comment_set.filter(approved_comment=True)
        return qs
        # return self.comments.filter(approved_comment=True)
