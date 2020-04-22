import getpass
import calendar
import os
import platform
import csv
import sys
import urllib.request

from time import sleep
from .socialMediaCollector import SocialMediaCollector
from selenium import webdriver
from ..utils.utils import Utility
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# -------------------------------------------------------------
# -------------------------------------------------------------



class FacebookCollector(SocialMediaCollector):
	
	def __init__(self):
		super(FacebookCollector, self).__init__()
		self.current_scrolls = 0
		self.utils = Utility(self.driver)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

	def scrap_profile(self,ids):

		
		writer = csv.writer(open(self.utils.file_name2, 'a', encoding='utf-8'))
		#writer.writerow(['Name','Overview','Work and Education','Places Lived', 'Contact and Basic Info','Family and Relationships','Details About','Life Events','Posts'])

		
		#execute for all profiles given in input.txt file
		while True:
			for id in ids:
		
				self.driver.get(id)
				name = id.split("/")[-1].replace("."," ")
				name = ''.join(e for e in name if (e.isalnum() or e==" "))
				url = self.driver.current_url
				id = self.utils.create_original_link(url)
			
				print("\nScraping:", id)
			
				print("----------------------------------------")
				print("About:")
				# setting parameters for scrap_data() to scrap the about section
				scan_list = [None] * 7
				section = self.utils.section_about
				elements_path = ["//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul/li/div/div[2]/div/div"] * 7
				file_names = ["Overview.txt", "Work and Education.txt", "Places Lived.txt", "Contact and Basic Info.txt",
							"Family and Relationships.txt", "Details About.txt", "Life Events.txt"]
				save_status = 3

				list_about = self.utils.scrap_data(id, scan_list, section, elements_path, save_status, file_names)
				print("About Section Done")
			
				# ----------------------------------------------------------------------------
				print("----------------------------------------")
				print("Posts:")
				#setting parameters for scrap_data() to scrap posts
				scan_list = [None]
				section = []
				elements_path = ['//div[@class="_5pcb _4b0l _2q8l"]']	
				
				file_names = ["Posts.txt"]
				save_status = 4
				
				list_posts = self.utils.scrap_data(id, scan_list, section, elements_path, save_status, file_names)
				print("Posts(Statuses) Done")
		
				#Writing in a csv file	
						
				writer.writerow([name,list_about[0],list_about[1],list_about[2],list_about[3],list_about[4],list_about[5],list_about[6],list_posts[0]])
		
				print("----------------------------------------")

				# ----------------------------------------------------------------------------
		
				print("\nProcess Completed.")
				sleep(3600)
		
		return


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

	def main(self):

		print("Filling input file")
		#self.utils.fill_input_file()
		ids = ["https://en-gb.facebook.com/" + line.split("/")[-1] for line in open("/home/sartharion/Bureau/stage/POO/com/utils/files/input_facebook.txt", newline='\n')]
		
		if len(ids) > 0:	
			print("\nStarting Scraping...")
		
			self.login()
			self.scrap_profile(ids)
			self.driver.close()
		else:
			print("Input file is empty..")


# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------


