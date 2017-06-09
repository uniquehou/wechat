from django.shortcuts import render
from django.http import HttpResponse
from random import random
from .models import Book_type, User, Book

def index(request):
	return render(request, 'library/index.html')

def login(request):
	if request.method == "POST":
		user = User.objects.get(mobile="request.POST['mobile']");
		if password == request.POST['password']:
			request.SESSION['name'] = user.name
		else:
			return render(request, 'library/login.html', {'error': 'error'})
		pass
	else:
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
	return render(request, 'library/user.html')

def favorite(request):
	if request.SESSION.get('name', False):
		user = User.objects.get(name=request.SESSION.get('name'))
		user.favorite += "%s " % request.GET['id']
		user.save()
	else:
		return render(request, 'library/login.html')





	
# 用户注册
# 推荐阅读
# 还书提醒