from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from random import random
from urllib.parse import quote
from .models import Book_type, User, Book

def index(request):
	return render(request, 'library/index.html')

def login(request):
	if request.method == "POST":
		user = User.objects.get(mobile=request.POST['mobile']);
		if user.passwd == request.POST['password']:
			request.session['id'] = user.id
			request.session['name'] = user.name if len(user.name) else user.nickname
			request.session['openid'] = user.openid
			request.session['img'] = user.headimgurl
			return render(request, 'library/user.html')
		else:
			return render(request, 'library/login.html', {'error': 'error'})
	else:
		# get userinfo

		return render(request, 'library/login.html')

def classification(request):
	if request.GET.get('id'):
		t = Book_type.objects.get(id=request.GET['id'])
		book = t.book_set.all()
		data = {'book_a': book[::3], 'book_b': book[1::3], 'book_c': book[2::3], 'class': t}
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
			'about_a': about.pop(int(random()*len(about))),
			'about_b': about.pop(int(random()*len(about))),
			'about_c': about.pop(int(random()*len(about))),
			}
	return render(request, 'library/book_detail.html', data)

def user(request):
	if request.session.get('name', False):
		data = {'name': request.session['name'], 'image': request.session['img']}
		return render(request, 'library/user.html', data)
	else:
		return render(request, 'library/login.html')

def favorite(request):
	if request.GET.get('id'):
		with connection.cursor() as cursor:
			cursor.execute("update library_user set favorite = favorite + '%s ' where id = %s" % (request.GET['id'], request.session['id']))
	else:
		favorite_book = User.objects.get(id=request.session['id']).split()
		books = Book.objects.filter(id__in=favorite_book)
		data = {'books':books}
		return render(request, 'library/favorite.html', data)

def borrow_column(request):
	if request.GET.get('id'):
		with connection.cursor() as cursor:
			cursor.execute("update library_user set borrow_column = concat(borrow_column, '%s ') where id = %s" % (request.GET['id'], request.session['id']))
		return HttpResponseRedirect(reverse('library:borrow_column'))
	else:
		borrow_column_book = User.objects.get(id=request.session['id']).borrow_column.split()
		# return HttpResponse(borrow_column_book)
		books = Book.objects.filter(id__in=borrow_column_book)
		data = {'books':books}
		return render(request, 'library/borrow_column.html', data)

def borrow(request):
	# with connection.cursor as cursor:
	# 	cursor.execute("update library_book set inventory = inventory - 1 where id = %s" % request.GET['id'])
	# 	cursor.execute("update library_user set book = concat(book, '%s ') where id = %s" % (request.GET['id'], request.session['id']))
	# 	cursor.execute("update library_user set borrow_column = replace(borrow_column. '%s ', '') where id = %s" % (request.GET['id'], request.session['id']))
	return HttpResponseRedirect(reverse('library:borrow_column'))

# show borrowed book
def borrowed(request):
	books = Book.objects.filter(id__in = User.objects.get(id=request.session['id']).books.split())
	data = {'books': books}
	return render(render, 'library/borrowed.html')

def backbook(request):
	with connection.cursor as cursor:
		cursor.execute("update library_book set inventory = inventory + 1 where id = %s" % request.GET['id'])
		cursor.execute("update library_user set book = replace(book. '%s ', '') where id = %s" % (request.GET['id'], request.session['id']))
	return HttpResponseRedirect(reverse('library:borrowed'))




	
# 用户注册
# 推荐阅读
# 还书提醒