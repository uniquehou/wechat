from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from random import random
from urllib.parse import quote
from .models import Book_type, User, Book

def index(request):
	return render(request, 'library/index.html')

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
		book = Book.objects.filter(name__contains=request.POST['search'].strip())
		if len(book) == 0:
			data = {'error': True}
		else:
			data = {'book_a': book[::3], 'book_b': book[1::3], 'book_c': book[2::3]}
		return render(request, 'library/search.html', data)
	else:
		return render(request, 'library/search.html')

def book_detail(request):
	book = Book.objects.get(id=request.GET['id'])
	about = list(book.type_id.book_set.all())
	data = {'book': book, 
			'about': about
			}
	return render(request, 'library/book_detail.html', data)
