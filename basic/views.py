from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from library.models import User
import requests
from datetime import datetime
from urllib.parse import quote
from .verify import *

def test(request):	
	user = User.objects.create(name=str(datetime.now()), passwd='test')
	return HttpResponse(user.name)

def getCodeUrl(requests):
	appid = "wx2fab5d8fc63cdcee"
	# redirect_url = quote('http://www.unihyj.cn' + request.path)
	redirect_url = "http%3a%2f%2fwww.unihyj.cn%2fbasic%2flogin"
	url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect" % (appid, redirect_url)
	return HttpResponse(url)

def login(request):
	appid = "wx2fab5d8fc63cdcee"
	secret = "e469f04bc8ae06b60f6a40215e46de01"
	code = request.GET['code']
	access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (appid, secret, code)
	new_access_token = requests.get(access_token_url)
	access_token = new_access_token.json().get('access_token')
	openid = new_access_token.json().get('openid')
	userinfo_url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s" % (access_token, openid)
	userinfo = requests.get(userinfo_url)

    # whether user sign
	try:
		user = User.objects.get(openid = userinfo.json().get(openid))
	except:
		user = User.objects.create(
			openid = userinfo.json().get('openid'),
			nickname = userinfo.json().get('nickname'),
			sex = userinfo.json().get('sex'),
			language = userinfo.json().get('language'),
			city = userinfo.json().get('city'),
			province = userinfo.json().get('province'),
			country = userinfo.json().get('country'),
			headimgurl = userinfo.json().get('headimgurl'),
			privilege = userinfo.json().get('privilege'),
		)

    # user infomation into session
	request.session['id'] = user.id
	request.session['name'] = user.name if len(user.name) else user.nickname
	request.session['openid'] = user.openid
	request.session['img'] = user.headimgurl
	return HttpResponseRedirect(reverse('library:user'))

def scanQRCode(request):
	token = getToken(1)
	jsapi = requests.get("https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % token).json()['ticket']
	sign = Sign(jsapi, 'http://www.unihyj.cn/basic/scanQRCode/')
	data = {'sign': sign.sign(), 'appId': 'wx2fab5d8fc63cdcee'}
	return render(request, 'basic/scanQRCode.html', data)

def getToken(request):
	AppID = 'wx2fab5d8fc63cdcee'
	AppSecret = 'e469f04bc8ae06b60f6a40215e46de01'
	url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (AppID, AppSecret)
	access_token = requests.get(url)
	if isinstance(request, int):
		return access_token.json()['access_token']
	else:
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
	    "button": [
	        {
	            "type": "scancode_push", 
	            "name": "借书", 
	            "key": "borrow"
	        }, 
	        {
	            "type": "view", 
	            "name": "图书馆", 
	            "url": "http://www.unihyj.cn/library"
	        }, 
	        {
	            "type": "view", 
	            "name": "还书", 
	            "url": "http://www.unihyj.cn/backbook"
	        }
	    ]
	}"""
	access_token = getToken()
	return HttpResponse(access_token)
	url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
	r = requests.post(url, data=data)
	return HttpResponse(r.text)

def error(request):
	return render(request, 'basic/error.html')