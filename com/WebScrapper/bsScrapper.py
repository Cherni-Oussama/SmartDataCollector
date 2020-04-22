import bs4 as bs
import urllib.request


class BsScrapper:


	def main(self):

		source = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()

		soup = bs.BeautifulSoup(source,'lxml')


		#If you do print(soup) and print(source), it looks the same, but the source is just plain the response data, and the soup is an object that we can actually interact with, by tag, now, like so:


		# title of the page
		print(soup.title)

		# get attributes:
		print(soup.title.name)

		# get values:
		print(soup.title.string)

		# beginning navigation:
		print(soup.title.parent.name)

		# getting specific values:
		print(soup.p)

		print(soup.find_all('p'))


		#We can also iterate through them:
	
		for paragraph in soup.find_all('p'):
		    print(paragraph.string)
		    print(str(paragraph.text))

		#Another common task is to grab links. For example:

		for url in soup.find_all('a'):
		    print(url.get('href'))

		#Finally, you may just want to grab text. You can use .get_text() on a Beautiful Soup object, including the full soup:
	
		print(soup.get_text())
