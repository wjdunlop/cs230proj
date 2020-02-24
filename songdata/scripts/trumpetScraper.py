import re
import urllib.request, urllib.error, urllib.parse

import requests
fullList = []

a = int(input("from\n> "))
b = int(input("to\n> "))
def retrieve(filename, pref):

	if filename != '\n':
		url = 'http://www.8notes.com'+filename
		print("FILE: ", filename)
		# print(url) 
		try:
			myfile = requests.get(url)
		except Exception as e:
			return url			


		name = re.findall('[\w_]*\.mid', filename)
		# 
		print("name")
		print(name[0])
		open('C:\\Users\\willi\\Desktop\\projects\\cs230proj\\songdata\\group\\'+str(pref)+'_'+name[0], 'wb').write(myfile.content)
		# print("downloaded")
				
		print("done!")

		return 0


user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'name': 'Michael Foord',
          'location': 'Northampton',
          'language': 'Python' }
headers = {'User-Agent': user_agent}

missedList = []

for i in range(a,b):

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

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('C:\\Users\\willi\\Desktop\\projects\\cs230proj\\songdata\\group')]
done = []
# print(onlyfiles)
for s in onlyfiles:
	f = re.findall('(\d{3,5})_', s)
	done+= f
print(done)

print(fullList)
ret = 0
for d in range(len(fullList)):
	i = fullList[d]
	print(d, " / ", len(fullList)) 
	f = re.findall('(\d{3,5})', i)
	# print(i)
	if f[0] in done:
		print('SKIP')
	if f[0] not in done:
		# print(i)
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
		# print("FOUND: ", find)
		ifGood = find[0]
		# print("retrieving")
		cont = True
			
		ret += 1
			
		# except Exception as e:
		# 	print('404, passing')
		# 	pass

		if cont:
			missed = retrieve(ifGood, i)


print('done, retrieved '+str(ret)+ " more")
# print(missedList)
# missed = open('missedList.txt', 'wb').write(sr+'\n' for sr in missedList)

		

