from django.shortcuts import render
from django.http import HttpResponse
import requests

def test(request):
	return HttpResponse('this is a test page')

def getToken(request):
	# AppID = 'wx454446d5decd4a00'
	AppID = 'wx2fab5d8fc63cdcee'
	# AppSecret = '6213c42c94e191a50148c6ff99c39a08'
	AppSecret = 'e469f04bc8ae06b60f6a40215e46de01'
	url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (AppID, AppSecret)
	access_token = requests.get(url)
	return HttpResponse(access_token.json()['access_token'])

def Token(request):
	try:
		signature = request.GET.get('signature')
		# timestamp = request.GET['timestamp']
		# echostr = request.GET['echostr']
		# nonce = request.GET['nonce']
	except:
		return HttpResponse('this request is error')
	else:
		return HttpResponse(signature+'abc')
		token = 'unique'
		li = list(token, timestamp, nonce)
		li.sort()
		import hashlib    # import hashlib
		sha1 = hashlib.sha1()
		map(sha1.update, list)
		hashcode = sha1.hexdigest()
		if hashcode == signature:
			return HttpResponse(echostr)

def menu(request):
	data = """{
			'button': [{
						'type': 'view',
						'name': '借阅详情',
						'url': 'http://www.taobao.com'
					},
					{
						'type': 'view',
						'name': '借阅室',
						'url': 'http://www.taobao.com'
					},
					{
						'type': 'view',
						'name': '还书',
						'url': 'http://www.taobao.com'
					}]
		}"""
	access_token = getToken()
	return HttpResponse(access_token)
	url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
	r = requests.post(url, data=data)
	return HttpResponse(r.text)

