from ..utils.utils import Utility
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep

class SocialMediaCollector:
	
	def __init__(self):
		self.driver = webdriver.Chrome(executable_path="/home/sartharion/Bureau/stage/POO/com/utils/chromedriver")	
		self.utils = Utility(self.driver)	
	
	#Login function for Facebook and Linkedin
	def login(self):
		if (self.__class__.__name__ == "LinkedinCollector"):
			self.driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
			
			username = self.driver.find_element_by_id('username')
			username.send_keys(self.utils.linkedin_username)
			sleep(0.5)
			
			password = self.driver.find_element_by_id('password')
			password.send_keys(self.utils.linkedin_password)
			sleep(0.5)
	
			sign_in_button = self.driver.find_element_by_xpath('//*[@type="submit"]')
			sign_in_button.click()
			sleep(0.5)
			
		elif (self.__class__.__name__ == "FacebookCollector"):
			options = Options()
			
			#  Code to disable notifications pop up of Chrome Browser
			options.add_argument("--disable-notifications")
			options.add_argument("--disable-infobars")
			options.add_argument("--mute-audio")
			# options.add_argument("headless")
			
			self.driver.get("https://en-gb.facebook.com")
			self.driver.maximize_window()
			
			# filling the form
			self.driver.find_element_by_name('email').send_keys(self.utils.facebook_login)
			self.driver.find_element_by_name('pass').send_keys(self.utils.facebook_password)
			
			# clicking on login button
			self.driver.find_element_by_id('loginbutton').click()

