from django.contrib import admin
from forum.models import *

class CategoryAdmin(admin.ModelAdmin):
	pass

class ForumAdmin(admin.ModelAdmin):
	list_display = ["title" , "category"]

class PostInline(admin.StackedInline):
	model = Post
	extra = 1

class ThreadAdmin(admin.ModelAdmin):
	list_display = ["title", "creator", "forum", "created"]
	list_filter = ["forum", "creator"]
	inlines = [PostInline]

class PostAdmin(admin.ModelAdmin):
	list_display = ["creator", "thread", "body", "created"]
	search_fields = ["creator", "body"]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)