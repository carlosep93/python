import sys
import urllib
from HTMLParser import HTMLParser
import mechanize
import cookielib
import re
import webbrowser

#sock = urllib.urlopen("https://www.facebook.com/?stype=lo&jlou=Afduq5yKvL_2euq0CPaoS0mMpWJN5jJpJaatX67IwQ8iGTYMmqH3R2K_Al2q1ivyyAmAxH5hwUJLa6CpUTrj-uEo&smuh=64571&lh=Ac_TPtZHW4mIFrKh")
#f = sock.read()
#sock.close()

friendslist = []
def connect():
	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	br.open("https://facebook.com")
	br.select_form(nr=0)
	#br.form['email'] = ''
	#br.form['pass'] = ''
	response = br.submit()
	return response.read()

def find(text):
	match = re.search(r"[^a-zA-Z](InitialChatFriendsList)[^a-zA-Z]", text)
	start = match.start(1) + 36
	fin = False
	while (start < len(text) and not fin):
		if text[start] == '}':
			fin = True
		elif text[start] == '"':
			aux = start
			start += 1
			while text[start] != '"':
				start += 1	
			friendslist.append(text[(aux+1):(start-2)])
			start += 1
		else:			
			start += 1
	
	return friendslist

def names():
	i = 0
	w = webbrowser.get('google-chrome')
	while i < 6:
		w.open_new_tab('https://facebook.com/' + friendslist[i])
		i += 1

		

f = connect()
find(f)
names()
