from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from embed_video.fields import EmbedVideoField
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify


def upload_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)


class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	draft = models.BooleanField(default=True)
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	tags = TaggableManager(blank=True)
	video = EmbedVideoField(max_length=200, null=True, blank=True)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field='image_height', width_field='image_width')
	image_width = models.IntegerField(default=100)
	image_height = models.IntegerField(default=100)
	slug = models.SlugField(unique=True)

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

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)#turn title to slug
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

pre_save.connect(pre_save_post_reciever, sender =Post)







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
