from com.SmCollectors.facebookCollector import FacebookCollector
from com.SmCollectors.linkedinCollector import LinkedinCollector
from com.SmCollectors.twitterCollector import TwitterCollector
from com.WebScrapper.bsScrapper import BsScrapper

class Scrapper:


	def __init__(self):
		#self.fb = FacebookCollector()
		#self.ln = LinkedinCollector()
		self.tw = TwitterCollector()
		self.bs = BsScrapper()
	
	def scrap(self):
		#self.ln.main()
		#self.fb.main()
		self.tw.main()
		#self.bs.main()

	
