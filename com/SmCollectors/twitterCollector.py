import json
import csv
import tweepy
import re

from ..utils.utils import Utility
from .socialMediaCollector import SocialMediaCollector
from .twitterConsumer import TwitterConsumer
from .twitterProducer import TwitterProducer

"""
INPUTS:
    consumer_key, consumer_secret, access_token, access_token_secret: codes 
    telling twitter that we are authorized to access this data
    hashtag_phrase: the combination of hashtags to search for
OUTPUTS:
    none, simply save the tweet info to a spreadsheet
"""

class TwitterCollector():

	def __init__(self):

		self.producer = TwitterProducer()
		self.consumer = TwitterConsumer()

    
	def main(self):

		while True:
			self.producer.main()
			print("Producer work done")
			self.consumer.main()
			print("Consumer's work done")
			sleep(3600)
