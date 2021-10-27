from django.db import models
from django.contrib.auth.models import User

URL_MAX_LENGTH = 2048

class Target(models.Model):
	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	country = models.CharField(max_length=32)
	birth_date = models.DateField()

	def __str__(self):
		return self.first_name + ' ' + self.last_name + ' (' + self.country + ')'

class DataProvider(models.Model):
	TYPE_BIOGRAPHY       = 'biography'
	TYPE_FAKE_NEWS       = 'fakenews'
	TYPE_INSTITUTIONAL   = 'institutional'
	TYPE_NEWS            = 'news'
	TYPE_PERSONAL        = 'personal'
	TYPE_SOCIAL_NETWORK  = 'socialnetwork'
	TYPE_VIDEOS          = 'videos'

	TYPE_CHOICES = (
		(TYPE_BIOGRAPHY,      'Biography'),
		(TYPE_FAKE_NEWS,      'Fake News'),
		(TYPE_INSTITUTIONAL,  'Institutional Website'),
		(TYPE_NEWS,           'News'),
		(TYPE_PERSONAL,       'Personal Website'),
		(TYPE_SOCIAL_NETWORK, 'Social Network'),
		(TYPE_VIDEOS,         'Videos'),
	)

	name = models.CharField(max_length=32)
	url = models.URLField(max_length=URL_MAX_LENGTH)
	source_type = models.CharField(max_length=32, choices=TYPE_CHOICES)

	def __str__(self):
		return self.name

class DataProviderSecret(models.Model):
	provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)
	name = models.CharField(max_length=32)
	data = models.CharField(max_length=512)

class DataSource(models.Model):
	TYPE_STORY = 'story'
	TYPE_PICTURE = 'picture'
	TYPE_VIDEO   = 'video'

	TYPE_CHOICES = (
		(TYPE_STORY,   'Article'),
		(TYPE_PICTURE, 'Picture'),
		(TYPE_VIDEO,   'Video'),
	)

	provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)
	source_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
	title = models.CharField(max_length=256)
	author = models.CharField(max_length=128)
	content = models.TextField()
	date = models.DateTimeField()
	language = models.CharField(max_length=32)
	official = models.BooleanField(default=False)
	screenshot = models.FileField()
	url = models.URLField(max_length=URL_MAX_LENGTH)
	verified = models.BooleanField(default=False)

class OnlinePresence(models.Model):
	provider = models.ForeignKey(DataProvider, on_delete=models.CASCADE)
	target = models.ForeignKey(Target, on_delete=models.CASCADE)
	url = models.URLField(max_length=URL_MAX_LENGTH)

class Picture(models.Model):
	picture = models.ImageField()
	source = models.ForeignKey(DataSource, on_delete=models.CASCADE)

class ProfilePicture(models.Model):
	picture = models.ImageField()
	target = models.ForeignKey(Target, on_delete=models.CASCADE)

	def __str__(self):
		return self.target.__str__()

class Tag(models.Model):
	tag = models.CharField(max_length=32)

	def __str__(self):
		return self.tag

class TagAssoc(models.Model):
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	source = models.ForeignKey(DataSource, on_delete=models.CASCADE)

class Verification(models.Model):
	source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
	date = models.DateTimeField()
	officialized = models.BooleanField(default=False)
	# TODO online_presence = 
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	verified = models.BooleanField(default=False)

class Video(models.Model):
	video = models.FileField()
	source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
