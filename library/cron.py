from datetime import datetime
import requests

def scheduled_job():
	requests.get('localhost/basic/test')

if __name__=='__main__':
	scheduled_job()
	
