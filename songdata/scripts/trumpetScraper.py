import re
import urllib.request, urllib.error, urllib.parse

import requests
fullList = []
def retrieve(filename, pref):
	if filename != '\n':
		url = 'http://www.8notes.com'+filename
		print("FILE: ", filename)
		# print(url) 
		myfile = requests.get(url)
		name = re.findall('[\w_]*\.mid', filename)
		# 
		print("name")
		print(name[0])
		open('C:\\Users\\willi\\Desktop\\projects\\cs230proj\\songdata\\group\\'+str(pref)+'_'+name[0], 'wb').write(myfile.content)
		# print("downloaded")
				
		print("done!")

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'name': 'Michael Foord',
          'location': 'Northampton',
          'language': 'Python' }
headers = {'User-Agent': user_agent}

for i in range(1,67):
	print(i,' ',len(fullList), flush = True, end = '\r')
	url = 'https://www.8notes.com/trumpet/sheet_music/?page='+str(i)+'&orderby=5d'
	rexp = 'href="/scores/(\d{3,6})'
	data = urllib.parse.urlencode(values)
	data = data.encode('ascii')
	req = urllib.request.Request(url, data, headers)
	response = urllib.request.urlopen(req)
	webContent = response.read()
	find = re.findall(rexp, str(webContent))
	fullList += find

for i in fullList: 
	print(i)
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	values = {'name': 'Michael Foord',
	          'location': 'Northampton',
	          'language': 'Python' }
	headers = {'User-Agent': user_agent}

	data = urllib.parse.urlencode(values)
	data = data.encode('ascii')
	url = 'http://www.8notes.com/scores/'+str(i)+'.asp?ftype=midi'

	req = urllib.request.Request(url, data, headers)

	   
	ifGood = ''
	cont = False
	rexp2 = '(/school/midi/trumpet/[\w\_\-\.]*.midi?)\"'
	print(url)
	response = urllib.request.urlopen(req)
	webContent = response.read()
	# print(webContent)
	find = re.findall(rexp2, str(webContent))
	# find += re.findall(rexp2, str(webContent))
	print("FOUND: ", find)
	ifGood = find[0]
	print("retrieving")
	cont = True
		
		
	# except Exception as e:
	# 	print('404, passing')
	# 	pass

	if cont:
		retrieve(ifGood, i)


		

