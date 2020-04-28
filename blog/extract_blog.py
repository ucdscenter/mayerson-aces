import json
import os
import requests
import info

class BlogExtract:
	def __init__(self, blog_name):
		self.name = blog_name
	def extract_posts(self, blog):
		return -1
	def extract_comments(self, post):
		return -1



if __name__ == '__main__':
	extractor = RedditExtract('Parenting', 'data/RC_2019-07')
	extractor.extract()
