from django.contrib import admin
from forum.models import Forum, Thread, Post

class ForumAdmin(admin.ModelAdmin):
	list_display = ['title' , 'sort_number']

class PostInline(admin.StackedInline):
	model = Post
	extra = 1

class ThreadAdmin(admin.ModelAdmin):
	list_display = ['title', 'creator', 'forum', 'created']
	list_filter = ['forum', 'creator']
	inlines = [PostInline]

class PostAdmin(admin.ModelAdmin):
	list_display = ['creator', 'thread', 'body', 'created']
	search_fields = ['creator', 'body']

admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)