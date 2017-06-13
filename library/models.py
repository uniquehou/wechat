from django.db import models

class User(models.Model):
	name = models.CharField(max_length=100)
	passwd = models.CharField(max_length=30)
	mobile = models.CharField(max_length=30)
	books = models.TextField(default='', blank=True)
	borrow_column = models.TextField(default='', blank=True)
	favorite = models.TextField(default='', blank=True)

class Book(models.Model):
	name = models.CharField(max_length=100)
	type_id = models.ForeignKey('Book_type', on_delete=models.CASCADE)
	author = models.CharField(max_length=100, default="unknown")
	version = models.CharField(max_length=10, blank=True)
	image = models.CharField(max_length=100, blank=True)
	inventory = models.SmallIntegerField(default=0)      # 库存
	public = models.CharField(max_length=100, default="unknown")
	public_time = models.DateField(auto_now=True)
	page_num = models.SmallIntegerField(blank=True, default=0)
	price = models.FloatField(default=0)
	ISBN = models.CharField(max_length=20, default="unknown")

	content_abstract = models.TextField(blank=True)
	author_abstract = models.TextField(blank=True)
	directory = models.TextField(blank=True)
	review = models.TextField(blank=True)

	Users = models.CharField(max_length=200, default='', blank=True)

class Book_type(models.Model):
	name = models.CharField('书名', max_length=30)
	note = models.CharField(max_length=30, blank=True)
	top_type = models.ForeignKey('Book_type', on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.name