import json
import csv
import tweepy
import re
from ..utils.utils import Utility
from .socialMediaCollector import SocialMediaCollector

"""
INPUTS:
    consumer_key, consumer_secret, access_token, access_token_secret: codes 
    telling twitter that we are authorized to access this data
    hashtag_phrase: the combination of hashtags to search for
OUTPUTS:
    none, simply save the tweet info to a spreadsheet
"""

class TwitterCollector(SocialMediaCollector):

	def __init__(self):

		super(TwitterCollector, self).__init__()	
		self.utils = Utility(self.driver)

	# load Twitter API credentials
		self.consumer_key = self.utils.consumer_key
		self.consumer_secret = self.utils.consumer_secret
		self.access_token = self.utils.access_token
		self.access_token_secret = self.utils.access_token_secret

		# Authorization and initialization
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(auth)

	
	#Function to get tweets by hasthags
	def search_for_hashtags(self,hashtag_phrase):
    	
    	#get the name of the spreadsheet we will write to
		fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))
		
    	#open the spreadsheet we will write to
		with open('%s.csv' % (fname), 'w', encoding='utf-8') as file:

			w = csv.writer(file)

        	#write header row to spreadsheet
			w.writerow(['timestamp', 'tweet_text', 'username', 'location', 'all_hashtags', 'followers_count'])

        	#for each tweet matching our hashtags, write relevant info to the spreadsheet
			for tweet in tweepy.Cursor(self.api.search, q=hashtag_phrase+' -filter:retweets', \
				                       lang="en", tweet_mode='extended').items(1000):
				w.writerow([tweet.created_at, tweet.full_text.replace('\n',' '), tweet.user.screen_name, tweet.user.location, [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])



	#Function to get tweets from a certain profile
	def get_user_tweets(self,name):


		# initialization of a list to hold all Tweets
		all_the_tweets = []


		print("screen name is", name)
		# We will get the tweets with multiple requests of 200 tweets each
		try:
			new_tweets = self.api.user_timeline(screen_name=name, count=200)

			# saving the most recent tweets
			all_the_tweets.extend(new_tweets)

			# save id of 1 less than the oldest tweet
			oldest_tweet = all_the_tweets[-1].id - 1

			# grabbing tweets till none are left
			while len(new_tweets) > 0:

				# The max_id param will be used subsequently to prevent duplicates
				new_tweets = self.api.user_timeline(screen_name=name, count=200, max_id=oldest_tweet)

				# save most recent tweets
				all_the_tweets.extend(new_tweets)
	
				# id is updated to oldest tweet - 1 to keep track
				oldest_tweet = all_the_tweets[-1].id - 1
				print ('...%s tweets have been downloaded so far' % len(all_the_tweets))

			# transforming the tweets into a 2D array that will be used to populate the csv	
			outtweets = [[tweet.id_str, tweet.created_at,
			tweet.text] for tweet in all_the_tweets]

		#In case there is no twitter account
		except:
			print("No twitter account found")
			outtweets = ["No twitter account"]

		return outtweets

		
	def get_all_users_tweets(self,names):
	
		# Twitter allows access to only 3240 tweets via this method				
		#Preparing csv file
		writer = csv.writer(open(self.utils.file_name3, 'w', encoding='utf-8'))
		writer.writerow(['Name', 'Screen Name', 'tweets'])

	
		#Collecting tweets of each user
		for name in names:
			
			tweets = self.get_user_tweets(name.replace(" ",""))
			writer.writerow([name, name.replace(" ",""), tweets])
		
		print("Scrapping done")

		

    
	def main(self):

		#fill input file
		self.utils.fill_input_file_twitter()
		
		#Get all the screen names
		names = [line.rstrip() for line in open("/home/sartharion/Bureau/stage/POO/com/utils/files/input_twitter.txt")]
		
		if len(names) > 0:	

			print("\nStarting Scraping...")
			self.get_all_users_tweets(names)

		else:
			print("Input file is empty..")

