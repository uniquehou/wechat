from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from random import random
from urllib.parse import quote
from .models import Book_type, User, Book

def index(request):
	books = Book.objects.all()
	data = {"books": books}
	return render(request, 'library/index.html', data)

def classification(request):
	if request.GET.get('id'):
		t = Book_type.objects.get(id=request.GET['id'])
		books = t.book_set.all()
		data = {'books': books, 'class': t}
	else:
		classes = Book_type.objects.all()
		data = {'classes': [x for x in classes if not bool(x.top_type_id)]}
	return render(request, 'library/classification.html', data)
	
def search(request):
	if request.POST.get('search'):
		books = Book.objects.filter(name__contains=request.POST['search'].strip())
		if len(books) == 0:
			data = {'error': True}
		else:
			data = {"books": books}
		return render(request, 'library/search.html', data)
	else:
		return render(request, 'library/search.html')

def book_detail(request):
	book = Book.objects.get(id=request.GET['id'])
	about = list(book.type_id.book_set.all())
	favorite = 1 if str(request.GET['id']) in User.objects.get(id=request.session['id']).favorite else 0
	data = {'book': book, 'about': about, 'favorite':favorite }
	return render(request, 'library/book_detail.html', data)
