from urllib.error import URLError
import urllib3
import json
import sys
from .film import Film

api_key = '&apikey=' ## Add your own APIkey here!
base_url = 'http://omdbapi.com/?tomatoes=true'

def get_film_by_title(title):
	url = base_url + '&t='
	print(url)
	sys.stdout.flush()
	http = urllib3.PoolManager()
	r = http.request('GET', url + title.replace(" ", "+") + api_key)
	try:
		response = r.data
		film = json.loads(response.decode('utf-8'))
		print(film)
		sys.stdout.flush()
		if not film['Response']: return None
		else: return Film(film)
	except URLError:
		print('No filmz :(( got an error code')
		sys.stdout.flush()
		return None

def get_film_by_id(id):
	url = base_url + '&i='
	http = urllib3.PoolManager()
	r = http.request('GET', url + id + api_key)
	try:
		response = r.data
		film = json.loads(response.decode('utf-8'))
		if not film['Response']: return None
		else: return Film(film)
	except URLError:
		print('No filmz :(( got an error code')
		sys.stdout.flush()
		return None
