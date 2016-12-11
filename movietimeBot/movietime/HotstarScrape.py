from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re
from pyvirtualdisplay import Display
import time
import urllib

response = ''


class myScraper(object):
	def __init__(self,movie):
		movie_input = re.sub(' ','%20',movie)
		self.url = "http://www.hotstar.com/search?q="+movie_input
		print (self.url)
		# self.url = url_final
		self.display = Display(visible=0, size=(800, 600))
		self.display.start()

	# browser = webdriver.Firefox() #REVIEWsudo apt-get -y install build-essential python-dev libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev

	# browser.set_window_size(1120, 550)

	def scrape(self):
		try:
			browser = webdriver.Firefox()
			browser.get(self.url)
			time.sleep(3)

			# browser.find_element_by_xpath('//*[@id="app-main-view"]/div/div[1]/div/div[1]/h3')

			# element_to_hover_over = browser.find_element_by_xpath('//*[@id="app-main-view"]/div/div[2]/div/hs-cards-directive/article/a/div[3]')
			# hover = ActionChains(browser).move_to_element(element_to_hover_over)
			# hover.perform()
			# time.sleep(2)
			# name = browser.find_element_by_xpath('//*[@id="tooltip-container"]/p[2]')
			# print name.text()

			# browser.find_element_by_xpath('//*[@id="autoCompleteSearchId"]').send_keys(movie)
			browser.find_element_by_xpath('//*[@id="app-main-view"]/div/div[2]/div/hs-cards-directive/article/a/div[3]').click()


			movies = BeautifulSoup(browser.page_source, "html.parser")
			name= movies.text.lower()
			# print name
			# time.sleep(2)
			# try:
			# 	movie_name = browser.find_element_by_xpath('//*[@id="title-card-undefined-0"]').click()
			# 	time.sleep(2)
			# 	movies = BeautifulSoup(browser.page_source, "html.parser")
			# 	name= movies.text.lower()
			# 	# movie_t = browser.find_element_by_class_name('title has-jawbone-nav-transition')
			# 	# print movie_t
			# 	# movie_text = browser.find_element_by_class_name('title has-jawbone-nav-transition').text()
			# 	# print movie_text
			# except Exception as e:
			# 	pass
			#
			# # browser.find_element_by_xpath('//*[@id="hdPinTarget"]/div/div[3]/div/div').click()
			# # browser.find_element_by_xpath('//*[@id="hdPinTarget"]/div/div[3]/div/div[2]/ul[3]/li[3]/a').click()
			# # # if 'var searchJson =' in movies_list.text:
			# #
			# # # match = re.search(r'var searchJson =', list, re.I)
			# # # match_end = re.search(r'var thumbImageUrl', list, re.I)
			# # # movies_block = list[match.start():match_end]
			# # # print movies_block
			# #
			# #
			self.display.stop()
			browser.quit()
			if movie in name:
				response = 'Available'
			# #
			# # else :
			# # 	browser.find_element_by_xpath('//*[@id="tabs"]/li[2]/a').click()
			# # 	movies_list_cs = BeautifulSoup(browser.page_source, "html.parser")
			# # 	if movie in movies_list_cs.text.lower():
			# # 		response = movie + ' is coming soon on PVR'
			else :
				response = 'Not Available'
			# # #
			print response
			return response
			# # browser.find_element_by_id('webId').send_keys(username)
			# # browser.find_element_by_id('password').clear()
			# # browser.find_element_by_id('password').send_keys(password)
			# # browser.find_element_by_id('searchBtn').submit()
			# # wait = WebDriverWait(browser, 10)
			# # wait.until(lambda driver: driver.find_element_by_id('previewPrefDialog'))
			#
		except :
			print 'Hotstar Except BLOCK'
			response = 'Not Available'
			return response

if __name__ == '__main__':
	scraper = myScraper('jolly llb')
	scraper.scrape()
