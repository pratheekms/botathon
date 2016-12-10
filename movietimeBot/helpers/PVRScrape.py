from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from pyvirtualdisplay import Display

class myScraper(object):
	def __init__(self,movie):
		self.url = "http://www.pvrcinemas.com/nowshowing/Bengaluru"
		self.display = Display(visible=0, size=(800, 600))
		self.display.start()

	# browser = webdriver.Firefox() #REVIEWsudo apt-get -y install build-essential python-dev libcurl4-nss-dev libsasl2-dev libsasl2-modules maven libapr1-dev libsvn-dev

	# browser.set_window_size(1120, 550)

	def scrape(self):
		try:
			browser = webdriver.Firefox()
			browser.get(self.url)
			# WebDriverWait(browser, 10)
			browser.find_element_by_id('more-ns').click()
			movies_list_ns = BeautifulSoup(browser.page_source, "html.parser")
			# list= movies_list.text
			# if 'var searchJson =' in movies_list.text:

			# match = re.search(r'var searchJson =', list, re.I)
			# match_end = re.search(r'var thumbImageUrl', list, re.I)
			# movies_block = list[match.start():match_end]
			# print movies_block


			if movie in movies_list_ns.text.lower():
				response = 'is now showing on PVR'

			else :
				browser.find_element_by_xpath('//*[@id="tabs"]/li[2]/a').click()
				movies_list_cs = BeautifulSoup(browser.page_source, "html.parser")
				if movie in movies_list_cs.text.lower():
					response = 'is coming soon on PVR'
				else :
					response = 'not available on PVR'

			self.display.stop()
			browser.quit()
			print response
			return response
			# browser.find_element_by_id('webId').send_keys(username)
			# browser.find_element_by_id('password').clear()
			# browser.find_element_by_id('password').send_keys(password)
			# browser.find_element_by_id('searchBtn').submit()
			# wait = WebDriverWait(browser, 10)
			# wait.until(lambda driver: driver.find_element_by_id('previewPrefDialog'))
		except :
			print 'PVR Except BLOCK'
			response = 'not available on PVR'
			return response


if __name__ == '__main__':
	scraper = myScraper()
	scraper.scrape()
