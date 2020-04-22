from scrapper import Scrapper
from merger import Merger
from JsonParser import Parser
from pymongo import MongoClient
import json
from bson import json_util


def main():
	scrapper = Scrapper()
	merger = Merger()
	parser = Parser()
	client = MongoClient('localhost', 27017)
	db = client['Data']
	collection_socialmedia = db['socialmedia']

	#Begin real time collecting
	while True: 
		scrapper.scrap()	
		merger.main()
		parser.main()	
		sleep(3600)
		
		#Storing to mangoDB
		f = open( '/home/sartharion/Bureau/stage/POO/data.json', 'r')  
		file_data = json.load(f)
		collection_socialmedia.delete_many({})
		collection_socialmedia.insert_many(file_data)		
	
	client.close()

if __name__ == '__main__':
    main()
