from django import forms
from django.forms import ModelForm
from forum.models import Post, Thread

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude= ['creator', 'thread']

class ThreadForm(PostForm):
	class Meta:
		model = Thread
		exclude = ['creator', 'forum']