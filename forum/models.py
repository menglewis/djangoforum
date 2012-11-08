from django.db import models
from django.contrib.auth.models import User
from string import join



class Category(models.Model):
	title = models.CharField(max_length=60)
	
	class Meta:
		verbose_name_plural = "Categories"

	def __unicode__(self):
		return self.title

class Forum(models.Model):
	title = models.CharField(max_length=60)
	category = models.ForeignKey(Category)
	
	def __unicode__(self):
		return self.title

	def num_posts(self):
		return sum([thread.num_posts() for thread in self.thread_set.all()])

	def last_post(self):
		if self.thread_set.count():
			last_post = None
			for thread in self.thread_set.all():
				last = thread.last_post()
				if last:
					if not last_post:
						last_post = last
					elif last.created > last_post.created:
						last_post = last
			return last_post

class Thread(models.Model):
	title = models.CharField(max_length=60)
	creator = models.ForeignKey(User, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	forum = models.ForeignKey(Forum)
	
	def __unicode__(self):
		return u"%s - %s" % (self.creator, self.title)

	def num_posts(self):
		return self.post_set.count()

	def num_replies(self):
		return self.post_set.count() - 1

	def last_post(self):
		return self.post_set.order_by('created')[0]

class Post(models.Model):
	creator = models.ForeignKey(User, blank=True, null=True)
	thread = models.ForeignKey(Thread)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return u"%s - %s" % (self.creator, self.thread)

	def short(self):
		return u"%s\n%s" % (self.thread, self.created)