""" filename: utils.py """

import getpass
import calendar
import os
import platform
import csv
import sys
import urllib.request

from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# whether to download photos or not
download_uploaded_photos = True
download_friends_photos = True

# whether to download the full image or its thumbnail (small size)
# if small size is True then it will be very quick else if its false then it will open each photo to download it
# and it will take much more time
friends_small_size = True
photos_small_size = True
	
scroll_time = 5
old_height = 0
total_scrolls = 50

class Utility:
	
	
	#Linkedin div classes :
	name_path = '//*[starts-with(@class,"inline t-24 t-black t-normal break-words")]/text()'
	college_path = '(//*[starts-with(@class,"text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view")])[2]/text()'
	company_path = '//*[starts-with(@class,"text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view")]/text()'
	job_path = '//*[starts-with(@class,"mt1 t-18 t-black t-normal")]/text()'
	location_path = '//*[starts-with(@class,"t-16 t-black t-normal inline-block")]/text()'
	skills_path = '//*[starts-with(@class,"pv-skill-category-entity__name-text t-16 t-black t-bold")]/text()'
	organizations_path = '//*[starts-with(@class,"pv-entity__secondary-title")]/text()'

	# search query 
	search_query = 'site:linkedin.com/in/ AND "developer" AND "Tunisia"'

	#Topic Name
	topic_name = 'tweets'
	
	
	# file were scraped profile information will be stored  
	file_name = 'linkedin_results.csv'
	file_name2 = 'facebook_results.csv'
	file_name3 = 'twitter_results.csv'
	
	# login credentials
	linkedin_username = 'davidmz@live.fr'
	linkedin_password = 'Inchalah1.'
	
	#bahscrapperbah@gmail.com
	facebook_login = 'bahscrapperbah@gmail.com'
	facebook_password = 'inchalah.'

	#Twitter Api Credentials
	consumer_key = "mPeFBMnRXuWKpyv8UyA8bRYH0"
	consumer_secret = "RfSBd4VyG035FKcpVIuXYIgKc0VlTkgTVuabRCo0vFLdrDY8Wd"
	access_token = "245817827-jZDVhqjGaV0cOBl0860qgL9oMhKFjqNSbhjqKDeZ"
	access_token_secret = "CU7nwAywjMPtGcsdRjZTsUN2VeVD0DoKTvzfqJemITnCI"

	#Sections :	
	section_about = ["/about?section=overview", "/about?section=education", "/about?section=living",
						"/about?section=contact-info", "/about?section=relationship", "/about?section=bio",
						"/about?section=year-overviews"]


	def __init__(self,driver):
		self.driver = driver		

	# function to ensure all key data fields have a value
	def validate_field(self,field):
		if field is None:
			field="No result"
		return field

# -------------------------------------------------------------
# -------------------------------------------------------------

	def get_field(self,sel,path):
		field = sel.xpath(path).extract_first()
		if field:
			field = field.strip()
		return field
# -------------------------------------------------------------
# -------------------------------------------------------------

	def get_fields(self,sel,path):
		field = sel.xpath(path).getall()
		return field
# -------------------------------------------------------------
# -------------------------------------------------------------

	def next_page(self):
		next = self.driver.find_element_by_id('pnnext')
		next.send_keys(Keys.RETURN)
# -------------------------------------------------------------
# -------------------------------------------------------------

	def expand_skills(self):
		next = self.driver.find_element_by_xpath('//*[starts-with(@class,"pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar")]')
		next.send_keys(Keys.RETURN)
		sleep(3)
# -------------------------------------------------------------
# -------------------------------------------------------------
	def google_search(self,query,driver):
		driver.get('https:www.google.com')
		sleep(3)
		
		search_query = self.driver.find_element_by_name('q')
		search_query.send_keys(query)
		sleep(0.5)
		
		search_query.send_keys(Keys.RETURN)
		sleep(3)

# -------------------------------------------------------------
# -------------------------------------------------------------
		#AAAAAAAAAAAAA
	def fill_input_file(self):
		f = open("/home/sartharion/Bureau/stage/POO/com/utils/files/input_facebook.txt", "w")
		input_file = csv.DictReader(open("/home/sartharion/Bureau/stage/POO/linkedin_results.csv"))
		for row in input_file:
			f.write("https://en-gb.facebook.com/"+row["Name"].replace(" ",".")+"\n")

		f.close()


# -------------------------------------------------------------
# -------------------------------------------------------------

		#BBBBBBBBB
	def fill_input_file_twitter(self):
		f = open("/home/sartharion/Bureau/stage/POO/com/utils/files/input_twitter.txt", "w")
		input_file = csv.DictReader(open("/home/sartharion/Bureau/stage/POO/linkedin_results.csv"))
		for row in input_file:
			f.write(row["Name"]+"\n")

		f.close()


# -------------------------------------------------------------
# -------------------------------------------------------------

	def check_height(self):
		new_height = self.driver.execute_script("return document.body.scrollHeight")
		return new_height != old_height


# -------------------------------------------------------------
# -------------------------------------------------------------

	# helper function: used to scroll the page
	def scroll(self):
		global old_height
		current_scrolls = 0

		while (True):
			try:
				if current_scrolls == total_scrolls:
					return

				old_height = self.driver.execute_script("return document.body.scrollHeight")
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				WebDriverWait(self.driver, scroll_time, 0.05).until(lambda driver: self.check_height())
				current_scrolls += 1
			except TimeoutException:
				break

		return


# -------------------------------------------------------------
# -------------------------------------------------------------

# --Helper Functions for Posts

	def get_status(self,x):
		status = ""
		try:
			status = x.find_element_by_xpath(".//div[@class='_5wj-']").text
		except:
			try:
				status = x.find_element_by_xpath(".//div[@class='userContent']").text
			except:
				pass
		return status


	def get_div_links(self,x, tag):
		try:
			temp = x.find_element_by_xpath(".//div[@class='_3x-2']")
			return temp.find_element_by_tag_name(tag)
		except:
			return ""


	def get_title_links(self,title):
		l = title.find_elements_by_tag_name('a')
		return l[-1].text, l[-1].get_attribute('href')


	def get_title(self,x):
		title = ""
		try:
			title = x.find_element_by_xpath(".//span[@class='fwb fcg']")
		except:
			try:
				title = x.find_element_by_xpath(".//span[@class='fcg']")
			except:
				try:
					title = x.find_element_by_xpath(".//span[@class='fwn fcg']")
				except:
					pass
		finally:
			return title


	def get_time(self,x):
		time = ""
		try:
			time = x.find_element_by_tag_name('abbr').get_attribute('title')
			time = str("%02d" % int(time.split(", ")[1].split()[1]), ) + "-" + str(
				("%02d" % (int((list(calendar.month_abbr).index(time.split(", ")[1].split()[0][:3]))),))) + "-" + \
					time.split()[3] + " " + str("%02d" % int(time.split()[5].split(":")[0])) + ":" + str(
				time.split()[5].split(":")[1])
		except:
			pass
		
		finally:
			return time


	def extract_and_write_posts(self,elements, filename):
		
		result = ""		
		
		result += " TIME || TYPE  || TITLE || STATUS  ||   LINKS(Shared Posts/Shared Links etc) " + ","
			
		for x in elements:
			try:
				video_link = " "
				title = " "
				status = " "
				link = ""
				img = " "
				time = " "
				
				# time
				time = self.get_time(x)
				
				# title
				title = self.get_title(x)
				if title.text.find("shared a memory") != -1:
					x = x.find_element_by_xpath(".//div[@class='_1dwg _1w_m']")
					title = self.get_title(x)
					
				status = self.get_status(x)
				if title.text == self.driver.find_element_by_id("fb-timeline-cover-name").text:
					if status == '':
						temp = self.get_div_links(x, "img")
						if temp == '':  # no image tag which means . it is not a life event
							link = self.get_div_links(x, "a").get_attribute('href')
							type = "status update without text"
						else:
							type = 'life event'
							link = self.get_div_links(x, "a").get_attribute('href')
							status = self.get_div_links(x, "a").text
					else:
						type = "status update"
						if self.get_div_links(x, "a") != '':
							link = self.get_div_links(x, "a").get_attribute('href')

				elif title.text.find(" shared ") != -1:
					
					x1, link = self.get_title_links(title)
					type = "shared " + x1

				elif title.text.find(" at ") != -1 or title.text.find(" in ") != -1:
					if title.text.find(" at ") != -1:
						x1, link = self.get_title_links(title)
						type = "check in"
					elif title.text.find(" in ") != 1:
						status = self.get_div_links(x, "a").text
						
				elif title.text.find(" added ") != -1 and title.text.find("photo") != -1:
					type = "added photo"
					link = self.get_div_links(x, "a").get_attribute('href')
						
				elif title.text.find(" added ") != -1 and title.text.find("video") != -1:
					type = "added video"
					link = self.get_div_links(x, "a").get_attribute('href')
						
				else:
					type = "others"
					
				if not isinstance(title, str):
					title = title.text
					
					status = status.replace("\n", " ")
					title = title.replace("\n", " ")
						
					line = str(time) + " || " + str(type) + ' || ' + str(title) + ' || ' + str(status) + ' || ' + str(
						link) + " , "

				result += line

			except:
				pass

		if result:
			return result
		else:
			return "No result"


# -------------------------------------------------------------
# -------------------------------------------------------------


	def create_original_link(self,url):
		if url.find(".php") != -1:
			original_link = "https://en-gb.facebook.com/" + ((url.split("="))[1])
			
			if original_link.find("&") != -1:
				original_link = original_link.split("&")[0]

		elif url.find("fnr_t") != -1:
			original_link = "https://en-gb.facebook.com/" + ((url.split("/"))[-1].split("?")[0])
		elif url.find("_tab") != -1:
			original_link = "https://en-gb.facebook.com/" + (url.split("?")[0]).split("/")[-1]
		else:
			original_link = url
			
		return original_link


# -------------------------------------------------------------
# -------------------------------------------------------------


	def save_to_file(self,name, elements, status, current_section):
		"""helper function used to save links to files"""
		
		# status 3 = dealing with about section
		# status 4 = dealing with posts
		
				
		results = []

			# dealing with About Section
		if status == 3:
			results = elements[0].text
			if results:
				results = ','.join(results)
				results = results.replace(",","")
				results = results.replace("\n",",")
				return results
			else:
				return "No result"

			# dealing with Posts
		elif status == 4:
			result_posts = self.extract_and_write_posts(elements, name)
			return result_posts
					
			
		return


# ----------------------------------------------------------------	------------
# -----------------------------------------------------------------------------

# -------------------------------------------------------------
# -------------------------------------------------------------re python

	

	def scrap_data(self,id, scan_list, section, elements_path, save_status, file_names):
		"""Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
		
		page = []
		x = []
		
		if save_status == 4:
			page.append(id)
			
		for i in range(len(section)):
			page.append(id + section[i])
			
		for i in range(len(scan_list)):
			try:
				self.driver.get(page[i])
						
				if save_status != 3:
					self.scroll()
					
				data = self.driver.find_elements_by_xpath(elements_path[i])
				
				x.append(self.save_to_file(file_names[i], data, save_status, i))

			except:
				print("Exception (scrap_data)", str(i), "Status =", str(save_status), sys.exc_info()[0])

		if not x:
			x =["No result"] * 7
		
		return x


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

