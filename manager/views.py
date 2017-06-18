from django.shortcuts import render,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from library.models import *

def backbook(request):
	with connection.cursor as cursor:
		cursor.execute("update library_book set inventory = inventory + 1 where id = %s" % request.GET['id'])
		cursor.execute("update library_user set book = replace(book. '%s ', '') where id = %s" % (request.GET['id'], request.session['id']))
