from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from djangoforum.settings import MEDIA_ROOT, MEDIA_URL
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from forum.models import *
from forum.forms import PostForm, ThreadForm

def main(request):
	forums = Forum.objects.all()
	context = {"forums": forums, "user": request.user}
	return render_to_response("forum/list.html", context)

def add_csrf(request, ** kwargs):
	d = dict(user=request.user, ** kwargs)
	d.update(csrf(request))
	return d

def make_paginator(request, items, num_items):
	paginator = Paginator(items, num_items)
	try:
		page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		items=paginator.page(page)
	except (InvalidPage, EmptyPage):
		items = paginator.page(paginator.num_pages)
	return items

def forum(request, pk):
	threads = Thread.objects.filter(forum=pk).order_by('-created')
	threads = make_paginator(request, threads, 20)
	return render_to_response("forum/forum.html", add_csrf(request, threads=threads, pk=pk))

def thread(request, pk):
	posts = Post.objects.filter(thread=pk).order_by('created')
	posts = make_paginator(request, posts, 20)
	title = Thread.objects.get(pk=pk).title
	return render_to_response('forum/thread.html', add_csrf(request, posts=posts, pk=pk, title=title, 
		media_url=MEDIA_URL))

def post(request, post_type, pk):
	
	