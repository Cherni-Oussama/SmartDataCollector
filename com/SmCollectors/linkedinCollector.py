""" filename: LinkedinCollector.py """
import csv
from time import sleep
from selenium import webdriver
from .socialMediaCollector import SocialMediaCollector 
from selenium.webdriver.common.keys import Keys
from parsel import Selector

class LinkedinCollector(SocialMediaCollector):
	
	
	#Initializing the csv file
	def __init__(self):
		super(LinkedinCollector, self).__init__()
	

	
	
	#Function to search and scrap profiles
	def scrap_profiles(self):
		
		writer = csv.writer(open(self.utils.file_name, 'a', encoding='utf-8'))
		#writer.writerow(['Name','Job Title','Company','College', 'Location','skills','WorkPlaces and Organization','URL'])
		
		self.utils.google_search(self.utils.search_query,self.driver)
		for x in range(0,8): #+1 next time
			self.utils.next_page()
		
		for x in range(0,1):

			linkedin_urls = self.driver.find_elements_by_class_name('iUh30')
			linkedin_urls = [url.text for url in linkedin_urls]
			sleep(0.5)
		
			for linkedin_url in linkedin_urls:
			
				self.driver.get(linkedin_url)
				sleep(2)
				#self.utils.scroll()
				sel = Selector(text=self.driver.page_source)
			
				name = self.utils.get_field(sel,self.utils.name_path)
				name = ''.join(e for e in name if (e.isalnum() or e==" "))

					
				job_title = self.utils.get_field(sel,self.utils.job_path)
			
				college =  self.utils.get_field(sel,self.utils.college_path)
			
				company = self.utils.get_field(sel,self.utils.company_path)
			
				location = self.utils.get_field(sel,self.utils.location_path)
			
				linkedin_url =  self.driver.current_url

				#self.utils.expand_skills()

				skills = self.utils.get_fields(sel,self.utils.skills_path)
				sleep(2)	
				skills = [skill.strip() for skill in skills]
				skills = ','.join(skills)

				organizations = self.utils.get_fields(sel,self.utils.organizations_path)
				sleep(2)	
				organizations = [organization.strip() for organization in organizations]
				organizations = ','.join(organizations)
	
			
			
				#Validate the fields 
				name = self.utils.validate_field(name)
				job_title = self.utils.validate_field(job_title)
				company = self.utils.validate_field(company)
				college = self.utils.validate_field(college)
				location = self.utils.validate_field(location)
				linkedin_url = self.utils.validate_field(linkedin_url)
				organizations = self.utils.validate_field(organizations)
				skills = self.utils.validate_field(skills)
				writer.writerow([name,job_title,company,college,location,skills,organizations,linkedin_url])


	
	#main class
	def main(self):
		
		print("\nStarting Scraping...")
		self.login()
		#super(LinkedinCollector,self).login()
		self.scrap_profiles()
		self.driver.quit()


