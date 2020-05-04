from twitter_credentials import TOKENS
import twitter
import json
from datetime import datetime


class TwitterGetter:
	def __init__(self, token):
		
		self.api = twitter.Api(consumer_key=token["consumer_key"],
					  consumer_secret=token["consumer_secret"],
					  access_token_key=token["access_token"],
					  access_token_secret=token["access_secret"], 
					  sleep_on_rate_limit=True)
		self.dateFormat = '%a %b %d %H:%M:%S %z %Y'
		
		
	def get_hashtag(self, tag, size=100):
		page_size = 100
		if size < page_size:
			init_size = size
		else:
			init_size = page_size
		results = []

		onecall = tg.api.GetSearch(raw_query="q=%23"+ tag +"&result_type=recent&count=" + str(init_size))
		results.extend(onecall)
		
		max_id = onecall[len(onecall) - 1].AsDict()["id"]
		max_date = onecall[len(onecall) - 1].AsDict()["created_at"]
		while len(results) < size and len(onecall) > 1:
			print("Scrolling")
			print(max_id)
			print(max_date)
			print(len(onecall))
			onecall = tg.api.GetSearch(raw_query="q=%23"+ tag +"&result_type=recent&count=" + str(init_size) + "&max_id=" + str(max_id))
			results.extend(onecall)
			max_id = onecall[len(onecall) - 1].AsDict()["id"]
			max_date = onecall[len(onecall) - 1].AsDict()["created_at"]


		results = list(map(lambda x: x.AsDict(), results))
		#for x in results:
		#	print(x)
		print(len(results))
		return results

	def get_hashtags(self, tags, size=100):
		print(tags)
		for htag in tags:
			print("Getting " + htag)
			#f = open(, "w")
			res = self.get_hashtag(htag, size=size)
			with open("data/" + htag + ".json", "w") as f:
				json.dump(res, f)
			#json.dump(res, "data/" + htag + ".json")
		return 
	def get_user(self, user):
		return -1
	def get_users_posts(self, users):
		return -1
	def get_users_followers(self, users):
		#for user in followers:

		return -1
	def get_followers_list(self, user):
		return -1


def combine_json(json_names):
	bigjson = []
	for htag in json_names:
		with open("data/" + htag + ".json", "r") as f:
			hdata = json.load(f)
			bigjson.extend(hdata)
		print(len(bigjson))

	with open("data/" + "all_htags" + ".json", "w") as wf:
		json.dump(bigjson, wf)

if __name__ == "__main__":
	h_keywords = ['ACEs', 'traumainformed', 'ACEaware', 'AdverseChildhoodExperiences','TraumaResponsive','Resilience']
	u_keywords = ['ACEsConnection','DrBurkeHarris','CYWSanFrancisco','DocResilience','TreatingTrauma1','Reattachparent','ACEsAware','nctsn','CenterOnTrauma']
	#tg = TwitterGetter(TOKENS)
	#tg.get_hashtags(h_keywords, size=2000)
	"""t = tg.api.GetUserTimeline(screen_name='ACEsConnection', count=200)
	tweets = [i.AsDict() for i in t]
	for x in tweets:
		print(x)"""
	#f = tg.api.GetFollowerIDs(screen_name='ACEsConnection', total_count=50)
	#print(f)

	combine_json(h_keywords)
	
	#for r in results:
	#	print(r)
	#for i in f:
	#	print(i)