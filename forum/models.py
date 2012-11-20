from django.db import models
from django.contrib.auth.models import User
import markdown

class Forum(models.Model):
	title = models.CharField(max_length=60)
	sort_number = models.IntegerField()
	
	def __unicode__(self):
		return self.title

	def num_posts(self):
		return sum([thread.num_posts() for thread in self.thread_set.all()])

	def num_threads(self):
		return self.thread_set.count()

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
	body = models.TextField(blank=True, null=True)
	body_markdown = models.TextField()
	creator = models.ForeignKey(User, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	forum = models.ForeignKey(Forum)
	
	def __unicode__(self):
		return u'%s - %s' % (self.creator, self.title)

	def short(self):
		return u'%s\n%s' % (self, self.created.strftime('%Y-%m-%d, %I:%M %p'))

	def num_posts(self):
		# count the body of the thread as one post
		return self.post_set.count() + 1

	def num_replies(self):
		return self.post_set.count()

	def last_post(self):
		# returns last related Post; if none, returns the thread
		if self.post_set.count():
			return self.post_set.order_by('-created')[0]
		else:
			return self

	def last_post_time(self):
		if self.post_set.count():
			return self.post_set.order_by('-created')[0].created
		else:
			return self.created

	def save(self):
		self.body = markdown.markdown(self.body_markdown)
		super(Thread, self).save()

class Post(models.Model):
	creator = models.ForeignKey(User, blank=True, null=True)
	thread = models.ForeignKey(Thread)
	body = models.TextField(blank=True, null=True)
	body_markdown = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return u'%s' % self.thread

	def short(self):
		return u'%s\n%s' % (self.thread, self.created.strftime('%Y-%m-%d, %I:%M %p'))
	
	def save(self):
		self.body = markdown.markdown(self.body_markdown)
		super(Post, self).save()