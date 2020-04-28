from twitter_credentials import TOKENS
import twitter


class TwitterGetter:
	def __init__(self, token):
		self.api = twitter.Api(consumer_key=token["consumer_key"],
	                  consumer_secret=token["consumer_secret"],
	                  access_token_key=token["access_token"],
	                  access_token_secret=token["access_secret"])

	def get_hashtag(self, tag):

		return 
	def get_hashtags(self, tags):

		return -1
	def get_user(self, user):
		return -1
	def get_users(self, users):
		return -1
	def get_followers(self, user):
		return -1
	def get_followers_list(self, users):
		return -1

if __name__ == "__main__":
	h_keywords = ['ACEs', 'traumainformed', 'ACEaware', 'AdverseChildhoodExperiences','TraumaResponsive','Resilience']
	u_keywords = ['ACEsConnection','DrBurkeHarris','CYWSanFrancisco','DocResilience','TreatingTrauma1','Reattachparent','ACEsAware','nctsn','CenterOnTrauma']
	tg = TwitterGetter(TOKENS)
	"""t = tg.api.GetUserTimeline(screen_name='ACEsConnection', count=10)
	tweets = [i.AsDict() for i in t]
	for x in tweets:
		print(x)"""
	f = tg.api.GetFollowers(screen_name='ACEsConnection', count=200)
	print(f)