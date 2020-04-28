import json
import os
import bz2
import zstandard as zstd
import matplotlib.pyplot as plt
import pandas as pd

class RedditExtract:
	def __init__(self, subr, file, level='post'):
		self.subreddit = subr
		self.file = file
		self.level = level
		self.wfile = subr + file[7:]

	def extract(self, save=None):
		print(self.file)
		print(self.subreddit)
		print(self.wfile)
		count = 0
		with open(self.file) as df:
			with open(self.wfile, 'a+') as wf:
				while True:
					text = df.readline() 
					if not text:
						break
					comment = json.loads(text)
					if comment['subreddit'] == self.subreddit:
						if count % 50 == 0:
							print(count)
						count += 1
						wf.write(text)
	def get_wfile(self):
		return self.wfile

class RedditExamine:
	def __init__(self, fname):
		self.fname = fname


if __name__ == '__main__':
	#extractor = RedditExtract('Parenting', 'data/RC_2019-07')
	#extractor.extract()

	examiner = RedditExamine('Parenting_2019-07')



