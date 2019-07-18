from django.db import models
from django.conf import settings
from django.utils import timezone
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.safestring import mark_safe, SafeText
from markdown_deux import markdown
from django.utils.text import slugify
from dmlcomments.models import Comment
from .utils import get_read_time

from typing import Any, Union
from django.db.models import QuerySet, CharField


def upload_location(instance: "Post", filename: str) -> str:
    PostModel = instance.__class__
    latest_post = PostModel.objects.order_by("pk").last()
    if latest_post:
        new_id = latest_post + 1
    return f"{new_id}/{filename}"


class PostManager(models.Manager):
    def active(self, *args: Any, **kwargs: Any) -> QuerySet:
        # Post.objects.all() = super(PostManager, self).all()
        return (
            super(PostManager, self)
            .filter(draft=False)
            .filter(publish__lte=timezone.now())
        )


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    draft = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    read_time = models.TimeField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    video = EmbedVideoField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        height_field="image_height",
        width_field="image_width",
    )
    image_width = models.IntegerField(default=100)
    image_height = models.IntegerField(default=100)
    slug = models.SlugField(unique=True)
    post_comments = GenericRelation(Comment, related_query_name="post_comments")

    objects = PostManager()

    class Meta:
        ordering = ["-created_date", "-published_date"]

    def publish(self) -> None:
        self.published_date = timezone.now()
        self.draft = False
        self.save()

    def unpublish(self) -> None:
        self.published_date = self.created_date
        self.draft = True
        self.save()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("blog:post_detail", kwargs={"pk": self.pk})

    def get_markdown(self) -> str:
        text = self.text
        markdown_text = markdown(text)
        marked_safe_text: str = mark_safe(markdown_text)
        return marked_safe_text

    @property
    def comments(self) -> "QuerySet[Comment, Post]":
        instance = self
        qs: "QuerySet[Comment, Post]" = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self) -> ContentType:
        instance = self
        content_type: ContentType = ContentType.objects.get_for_model(
            instance.__class__
        )
        return content_type


def create_slug(
    instance: Post, new_slug: Union[str, SafeText, None] = None
) -> SafeText:
    slug_inp: Union[str, SafeText, CharField]
    # if give a slug, it uses that
    if new_slug is not None:
        slug_inp = new_slug
    # else it makes one from the title
    else:
        slug_inp = instance.title
    slug = slugify(slug_inp, allow_unicode=True)
    qs = Post.objects.filter(slug=slug).order_by("-id")
    qs_first = qs.first()
    qs_exists = qs.exists()
    # if slug given or made already exists, make new one
    if qs_exists and qs_first is not None:
        newer_slug = f"{slug}-{qs_first.id}"
        slug = create_slug(instance, new_slug=newer_slug)
    return slug


def pre_save_post_reciever(
    sender: Post, instance: Post, *args: Any, **kwargs: Any
) -> None:

    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.text:
        html_string = instance.text  # instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_reciever, sender=Post)


# Is this redundant to dmlcomments now?
class Comment(models.Model):
    post = models.ForeignKey(
        "dmlblog.Post", related_name="comments", on_delete=models.CASCADE
    )
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self) -> None:
        self.approved_comment = True
        self.save()

    def __str__(self) -> str:
        return self.text

    def approved_comments(self) -> "QuerySet[Comment]":
        # return self.comments.filter(approved_comment=True)
        return self.post.comments.filter(approved_comment=True)
