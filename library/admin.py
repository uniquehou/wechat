from django.contrib import admin
from .models import *

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('name', 'author', 'image', 'inventory', 'public', 'public_time', 'page_num', 'price', 'ISBN')
	search_field = ('name', 'auth')
	ordering = ('name', 'inventory')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	pass
	# list_display = ('name', 'passwd', 'mobile')
	# search_field = ('name', 'mobile')
	# ordering = ('name', )

@admin.register(Book_type)
class Book_typeAdmin(admin.ModelAdmin):
	list_display = ('name', 'note')
	search_field = ('name')
	ordering = ('top_type', )