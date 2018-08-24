import requests
import bs4 
import urllib.request
import time
import re
import xlrd
import xlsxwriter
import os
import sys

def getPages(url):
	response = requests.get(url)
	soup = bs4.BeautifulSoup(response.text,'html.parser')
	string = soup.find('div', class_="page-of-pages arrange_unit arrange_unit--fill")
	string = string.text
	pages = [int(s) for s in string.split() if s.isdigit()]
	return pages[1]

def getReviews(url):
	response = requests.get(url)
	soup = bs4.BeautifulSoup(response.text,'html.parser')
	string = soup.find_all('p', lang="en")
	return string

def getRatings(url):
	response = requests.get(url)
	soup = bs4.BeautifulSoup(response.text,'html.parser')
	ratings = ['i-stars i-stars--regular-5 rating-large',
				'i-stars i-stars--regular-4 rating-large',
				'i-stars i-stars--regular-3 rating-large',
				'i-stars i-stars--regular-2 rating-large',
				'i-stars i-stars--regular-1 rating-large']
	string = []
	for contents in soup.find_all('div', class_='review-content'):
		rating = contents.find('div', {'class':ratings})
		string.append(rating)
	ratings = []
	for i in string:
		ratings.append(i.attrs['title'])
	return ratings

def getDates(url):
	response = requests.get(url)
	soup = bs4.BeautifulSoup(response.text,'html.parser')
	string = soup.find_all('span', class_='rating-qualifier')
	return string

def getUsers(url):
	response = requests.get(url)
	soup = bs4.BeautifulSoup(response.text,'html.parser')
	string = []
	for contents in soup.find_all('div', class_='ypassport media-block'):
		#print(type(contents))
		user = contents.find('a', class_='user-display-name js-analytics-click')
		string.append(user)
	return string	

def writeFile(arr,file): # Open and write arr into file
	workbook = xlsxwriter.Workbook(file)
	worksheet = workbook.add_worksheet()
	for col, data in enumerate(arr):
		row = 0
		worksheet.write_column(row, col, data)
	workbook.close()	

print("Running!")		

branch = sys.argv[1]  #name of the branch
mainUrl = sys.argv[2]  #link to change for different branch

pages = getPages(mainUrl)

reviews_data = []
ratings_data = []
dates_data = []
users_data = []

for i in range(1,pages+1):  #change for unit test
	extend = '?start=' + (str)((i-1)*20)
	url = mainUrl + extend
	reviews_data.append(getReviews(url))
	ratings_data.append(getRatings(url))
	dates_data.append(getDates(url))
	users_data.append(getUsers(url))	

reviews = []
ratings = []
dates = []
users = []
for i in reviews_data:
	for j in i:
		reviews.append(j.text)

for i in ratings_data:
	for j in i:
		ratings.append(j)

for i in dates_data:
	for j in i:
		if "/" in j.text and "Previous" not in j.text:
			dates.append(j.text)

for i in users_data:
	for j in i:
		users.append(j.text)					

# for i in range(0,len(reviews)):
# 	print("User: " + users[i])
# 	print("Rating: " + ratings[i])
# 	print("Review: " + reviews[i])
# 	print("Data: "+ dates[i])
# 	print()	

datas = [users,ratings,reviews,dates]

fileName = branch + ".xlsx"

if os.path.exists(fileName):
	os.remove(fileName)

writeFile(datas,fileName)

print("Finish!")
