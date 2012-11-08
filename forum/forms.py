from django import forms
from django.forms import ModelForm
from forum.models import Post, Thread

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		include = ['body']

class ThreadForm(forms.ModelForm):
	class Meta:
		model = Thread
		include = ['title']