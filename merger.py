import csv
import pandas as pd


class Merger:

	def main(self):

		fb = pd.read_csv("facebook_results.csv")
		ln = pd.read_csv("linkedin_results.csv")
		tw = pd.read_csv("twitter_results.csv").drop(columns="Screen Name")
		merged1 = ln.merge(fb, on='Name')
		merged2 = merged1.merge(tw, on='Name')
		merged2.to_csv("output.csv", index=False)


