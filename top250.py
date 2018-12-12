#encoding=utf-8

import requests
from bs4 import BeautifulSoup as bs
import time
import numpy as np
from openpyxl import Workbook
import re

#取出评价人数
pattern = re.compile(r'([0-9]+)', re.DOTALL)

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'

headers = {
	'User-Agent':agent,
	'Host':'book.douban.com',
	'Referer':'https://book.douban.com',
	'Connection':'keep-alive',
}
filename = 'top250.xlsx'
url = 'https://book.douban.com/top250'

def GetContent(url):
	book_list = []
	while True:
		html = requests.get(url, headers = headers).text
		soup = bs(html, 'lxml')
		soup_list = soup.findAll('tr', {'class':'item'})
		time.sleep(np.random.rand()*10)
		for item in soup_list:
			finda = item.findAll('a')[1]
			href = finda.get('href')
			findp = item.findAll('p')
			pub_list = findp[0].string.strip().split('/')
			try:
				title = finda.string.strip()
			except:
				title0 = finda.get('title')
				title1 = finda.find('span').string.strip()
				title = title0 + title1
			try:
				author = '/'.join(pub_list[0:-3])
			except:
				author = '暂无'
			pub = '/'.join(pub_list[-3:])
			rating = item.find('span', {'class':'rating_nums'}).string
			people_num = item.find('span', {'class':'pl'}).string.strip()
			people_num = pattern.findall(people_num)[0]
			try:
				brief = findp[1].find('span').string
			except:
				brief = '暂无'
			book_list.append([title, float(rating), int(people_num), author, pub, href, brief])
		try:
			next_href = soup.find('span', {'class':'next'}).find('a').get('href')
			url = next_href
		except:
			break
	return book_list

def save_xlsx(book_list):
	wb = Workbook()
	ws = wb.create_sheet('top250', 0)
	ws.append(['序号', '书名', '评分', '评价人数', '作者', '出版信息', '链接', '简介'])
	count = 1
	for book in book_list:
		ws.append([count, book[0], book[1], book[2], book[3], book[4], book[5], book[6]])
		count += 1
	wb.save(filename)

def main():
	print("正在保存豆瓣top250:\n")
	book_list = GetContent(url)
	save_xlsx(book_list)
	print("完成！\n")

if __name__ == '__main__':
	main()
