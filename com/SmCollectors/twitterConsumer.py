import json
import csv
import tweepy
import re
from ..utils.utils import Utility
from .socialMediaCollector import SocialMediaCollector
from kafka import KafkaConsumer

"""
INPUTS:
    consumer_key, consumer_secret, access_token, access_token_secret: codes 
    telling twitter that we are authorized to access this data
    hashtag_phrase: the combination of hashtags to search for
OUTPUTS:
    none, simply save the tweet info to a spreadsheet
"""

class TwitterConsumer(SocialMediaCollector):

	def __init__(self):

		super(TwitterConsumer, self).__init__()	
		self.utils = Utility(self.driver)	
		self.consumer = KafkaConsumer(self.utils.topic_name,bootstrap_servers='localhost:9092',auto_offset_reset='earliest',enable_auto_commit=True)

		
	def get_all_users_tweets(self):
	
		#Preparing csv file
		writer = csv.writer(open(self.utils.file_name3, 'w', encoding='utf-8'))
		writer.writerow(['Name', 'Screen Name', 'tweets'])

		#Getting Kafka messages
		print("subscribing")
		#self.consumer.subscribe(self.utils.topic_name)

		#Collecting tweets of each user
		for tweet in self.consumer:
			tweet = str(tweet.value, 'utf-8', 'ignore')
			print ("tweets gotten")
			listed = tweet.split('#')
			name = listed[0]
			if listed[1] == 'No twitter account':
				writer.writerow([name, name.replace(" ",""), listed[1]])
			else:
				tweets = listed[1].split('||')
				final_tweets = [tweet.split('%') for tweet in listed[1]]
				writer.writerow([name, name.replace(" ",""), final_tweets])
			print("tweets written")
		
		print("Scrapping done")

		

    
	def main(self):

		

		print("\nGetting from kafka...")
		self.get_all_users_tweets()

		
		

