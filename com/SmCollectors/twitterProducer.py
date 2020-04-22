import json
import csv
import tweepy
import re
from ..utils.utils import Utility
from .socialMediaCollector import SocialMediaCollector
from kafka import KafkaProducer

"""
INPUTS:
    consumer_key, consumer_secret, access_token, access_token_secret: codes 
    telling twitter that we are authorized to access this data
    hashtag_phrase: the combination of hashtags to search for
OUTPUTS:
    none, simply save the tweet info to a spreadsheet
"""

class TwitterProducer(SocialMediaCollector):

	def __init__(self):

		super(TwitterProducer, self).__init__()	
		self.utils = Utility(self.driver)
		self.producer = KafkaProducer(bootstrap_servers='localhost:9092')

	# load Twitter API credentials
		self.consumer_key = self.utils.consumer_key
		self.consumer_secret = self.utils.consumer_secret
		self.access_token = self.utils.access_token
		self.access_token_secret = self.utils.access_token_secret

		# Authorization and initialization
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(auth)




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
			outtweets = [[tweet.id_str, tweet.created_at.strftime("%d-%b-%Y (%H:%M:%S.%f)"),
			tweet.text] for tweet in all_the_tweets]

		#In case there is no twitter account
		except:
			print("No twitter account found")
			outtweets = ["No twitter account"]

		return outtweets

		
	def get_all_users_tweets(self,names):
	
	
		#Collecting tweets of each user
		for name in names:
			
			tweets = self.get_user_tweets(name.replace(" ",""))	
			tweets = '||'.join('%'.join(v) for v in tweets)
			#Sending tweets via kafka
			tweets = name + '#' + tweets
			tweets_bytes = bytes(tweets, encoding='utf-8')
			self.producer.send(self.utils.topic_name, tweets_bytes)
			print("Tweets sent throught broker")
	
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

