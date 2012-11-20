from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from forum.models import Post, Thread, Forum
from forum.forms import PostForm, ThreadForm

def main(request):
	"View for the main page that lists the forums by specified sort number"
	forums = Forum.objects.all().order_by('sort_number')
	context = {'forums': forums, 'user': request.user}
	return render_to_response('forum/main.html', context)

def add_csrf(request, ** kwargs):
	"takes request and kwargs and creates a dictionary and handles the csrf token"
	csrf_update = dict(user=request.user, ** kwargs)
	csrf_update.update(csrf(request))
	return csrf_update

def make_paginator(request, items, num_items):
	"creates a paginator for an object"
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
	"View that displays the threads in a specific forum"
	forum = Forum.objects.get(pk=pk)
	# sort the threads by reverse order of the last post in each thread
	threads = list(Thread.objects.filter(forum=pk))
	threads.sort(key=lambda thread: thread.last_post_time())
	threads.reverse()
	
	threads = make_paginator(request, threads, 20)
	return render_to_response('forum/forum.html', add_csrf(request, forum=forum, threads=threads, pk=pk))

def thread(request, pk):
	"View that displays the posts in a specific thread"
	posts = Post.objects.filter(thread=pk).order_by('created')
	posts = make_paginator(request, posts, 20)
	thread = Thread.objects.get(pk=pk)
	return render_to_response('forum/thread.html', add_csrf(request, posts=posts, pk=pk, 
		thread=thread))

@login_required
def reply(request, pk):
	"View that handles POST request for a reply or renders the form for a reply"
	error = ''
	if request.method == 'POST':
		p = request.POST
		if p['body_markdown']:
			thread = Thread.objects.get(pk=pk)
			post = Post()
			form = PostForm(p, instance=post)
			post = form.save(commit=False)
			post.thread, post.creator = thread, request.user
			post.save()

			return HttpResponseRedirect(reverse('forum.views.thread', args=[pk]) + '?page=last')
		else:
			error = 'Please enter a Reply\n'

	thread = Thread.objects.get(pk=pk)
	post_form = PostForm()
	return render_to_response('forum/reply.html', add_csrf(request, thread=thread, 
		post_form=post_form, error=error, pk=pk))

@login_required
def new_thread(request, pk):
	"View that handles POST request for a new thread or renders the form for a new thread"
 	error = ''
 	if request.method == 'POST':
 		p = request.POST
 		if p['body_markdown'] and p['title']:
 			forum = Forum.objects.get(pk=pk)
 			thread = Thread()
 			form = ThreadForm(p, instance=thread)
 			thread = form.save(commit=False)
 			thread.forum, thread.creator = forum, request.user
 			thread.save()
 			
 			return HttpResponseRedirect(reverse('forum.views.thread', args=[thread.pk]))
 		else:
 			error = 'Please enter the Title and Body\n'

 	forum = Forum.objects.get(pk=pk)
 	thread_form = ThreadForm()
 	return render_to_response('forum/new_thread.html', add_csrf(request, forum=forum, 
 		thread_form=thread_form, error=error, pk=pk))
