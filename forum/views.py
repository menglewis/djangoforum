from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from djangoforum.settings import MEDIA_ROOT, MEDIA_URL
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from forum.models import Post, Thread, Forum, Category
from forum.forms import PostForm, ThreadForm
from django.contrib.auth.decorators import login_required

def main(request):
	forums = Forum.objects.all()
	context = {"forums": forums, "user": request.user}
	return render_to_response("forum/main.html", context)

def add_csrf(request, ** kwargs):
	csrf_update = dict(user=request.user, ** kwargs)
	csrf_update.update(csrf(request))
	return csrf_update

def make_paginator(request, items, num_items):
	paginator = Paginator(items, num_items)
	try:
		page = int(request.GET.get('page', '1'))
	except ValueError: 
		page = 1

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
	thread = Thread.objects.get(pk=pk)
	return render_to_response('forum/thread.html', add_csrf(request, posts=posts, pk=pk, 
		thread=thread))

@login_required
def reply(request, pk):
	error = ''
	if request.method == "POST":
		p = request.POST
		if p['body_markdown']:
			thread = Thread.objects.get(pk=pk)
			post = Post()
			form = PostForm(p, instance=post)
			post = form.save(commit=False)
			post.thread = thread

			#post = Post.objects.create(thread=thread, body=p['body'], creator=request.user)
			return HttpResponseRedirect(reverse('forum.views.thread', args=[pk]) + '?page=last')
		else:
			error = 'Please enter a Reply\n'

	thread = Thread.objects.get(pk=pk)
	post_form = PostForm()
	return render_to_response('forum/reply.html', add_csrf(request, thread=thread, 
		post_form=post_form, error=error, pk=pk))

@login_required
def new_thread(request, pk):
 	error = ''
 	if request.method == "POST":
 		p = request.POST
 		if p['body_markdown'] and p['title']:
 			forum = Forum.objects.get(pk=pk)
 			thread = Thread.objects.create(forum=forum, title=p['title'], 
 				body=p['body'], creator=request.user)
 			return HttpResponseRedirect(reverse('forum.views.thread', args=[thread.pk]))
 		else:
 			error = 'Please enter the Title and Body\n'

 	forum = Forum.objects.get(pk=pk)
 	thread_form = ThreadForm()
 	return render_to_response('forum/new_thread.html', add_csrf(request, forum=forum, 
 		thread_form=thread_form, error=error, pk=pk))
