from django.db import models
from django.conf import settings
from django.utils import timezone
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from django.utils.text import slugify
from dmlcomments.models import Comment
from .utils import get_read_time


def upload_location(instance, filename):
	PostModel = instance.__class__
	new_id = PostModel.objects.order_by("pk").last().id + 1
	return "%s/%s" %(new_id, filename)

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		#Post.objects.all() = super(PostManager, self).all()
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

class Post(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	title = models.CharField(max_length=200)
	text = models.TextField()
	draft = models.BooleanField(default=True)
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	read_time = models.TimeField(blank=True, null=True)
	tags = TaggableManager(blank=True)
	video = EmbedVideoField(max_length=200, null=True, blank=True)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field='image_height', width_field='image_width')
	image_width = models.IntegerField(default=100)
	image_height = models.IntegerField(default=100)
	slug = models.SlugField(unique=True)
	post_comments = GenericRelation(Comment, related_query_name='post_comments')

	objects = PostManager()

	class Meta:
		ordering = ["-created_date", "-published_date"]

	def publish(self):
		self.published_date = timezone.now()
		self.draft = False
		self.save()

	def unpublish(self):
		self.published_date = self.created_date
		self.draft = True
		self.save()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={"pk":self.pk})

	def get_markdown(self):
		text = self.text
		markdown_text = markdown(text)
		return mark_safe(markdown_text)

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title, allow_unicode=True)#turn title to slug
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()#check if slug exists
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

	if instance.text:
		html_string = instance.text  #instance.get_markdown()
		read_time_var = get_read_time(html_string)
		instance.read_time = read_time_var

pre_save.connect(pre_save_post_reciever, sender=Post)

class Comment(models.Model):
	post = models.ForeignKey('dmlblog.Post', related_name='comments')
	author = models.CharField(max_length=200)
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
