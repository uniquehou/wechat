from django.shortcuts import render,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from library.models import *
import basic

def borrow(request, book_id, user_id):
	if request.session.get('Type') == "manager":
		with connection.cursor() as cursor:
			cursor.execute("update library_book set inventory = inventory - 1 where id = %s" % book_id)
			cursor.execute("update library_user set books = concat(books, '%s ') where id = %s" % (book_id, user_id))
			cursor.execute("update library_user set borrow_column = replace(borrow_column, '%s ', '') where id = %s" % (book_id, user_id))
		return True
	else:
		return 'error'

def backbook(request, book_id, user_id):
	if request.session.get('Type') == "manager":
		with connection.cursor() as cursor:	
			cursor.execute("update library_book set inventory = inventory + 1 where id = %s" % book_id)
			cursor.execute("update library_user set books = replace(books, '%s ', '') where id = %s" % (book_id, user_id))
		return True
	else:
		return "error"

def user(request):
	data = basic.views.scanQRCode(1)
	return render(request, 'manager/user.html', data)
