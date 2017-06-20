from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from library.models import *
import os

def login(request):
	if request.method == "POST":
		user = User.objects.get(mobile=request.POST['mobile']);
		if user.passwd == request.POST['password']:
			request.session['id'] = user.id
			request.session['name'] = user.name if len(user.name) else user.nickname
			request.session['openid'] = user.openid
			request.session['img'] = user.headimgurl
			if user.Type == "manager":
				request.session['Type'] = 'manager'
				return HttpResponseRedirect(reverse('manager:user'))
			return HttpResponseRedirect(reverse('user:user'))
		else:
			return render(request, 'user/login.html', {'error': 'error'})
	else:
		return render(request, 'user/login.html')

def user(request):
	if request.session.get('name', False):
		data = {'name': request.session.get('name'), 'image': request.session.get('img')}
		return render(request, 'user/user.html', data)
	else:
		return render(request, 'user/login.html')

def information(request):
	user = User.objects.get(id=request.session.get('id'))
	data = dict()
	if request.method == "POST":
		user.name = request.POST['name']
		user.sex = 2 if request.POST.get('sex') else 1

		# save headimage
		try:
			file = request.FILES.get('headimgurl')
			file_name = str(request.session['id']) + '.jpg'
			file_url = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/images/headimg/', file_name)
			with open(file_url, 'wb') as f:
				f.write(file.read())
			user.headimgurl = '/static/images/headimg/' + file_name
		except:
			pass

		user.save()
		request.session['img'] = user.headimgurl
		request.session['name'] = user.name
		data['change'] = 'true'

	data["user"] = user
	return render(request, 'user/information.html', data)

def favorite(request):
	if request.session.get('name'):
		if request.GET.get('id'):
			with connection.cursor() as cursor:
				cursor.execute("update library_user set favorite = concat(favorite, '%s ') where id = %s" % (request.GET['id'], request.session['id']))
			return HttpResponseRedirect("/library/book_detail?id=%s" % request.GET['id'])
		else:
			favorite_book = User.objects.get(id=request.session['id']).favorite.split()
			books = Book.objects.filter(id__in=favorite_book)
			data = {'books':books}
			return render(request, 'user/favorite.html', data)
	else:
		return HttpResponseRedirect(reverse("user:login"))

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
		return render(request, 'user/borrow_column.html', data)

# show borrowed book
def borrowed(request):
	books = Book.objects.filter(id__in = User.objects.get(id=request.session['id']).books.split())
	data = {'books': books}
	return render(request, 'user/borrowed.html')

def backbook(request):
	books = User.objects.get(id=request.session.get('id')).books.split();
	books = Book.objects.filter(id__in = books)
	data = {'books': books}
	return render(request, 'user/backbook.html', data)

def order(request):
	return render(request, 'basic/error.html')
