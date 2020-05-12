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
		the_tag = tag.replace(".", "%2E").replace("/","%2F").replace("#", "%23")
		page_size = 100
		if size < page_size:
			init_size = size
		else:
			init_size = page_size
		results = []

		onecall = self.api.GetSearch(raw_query="q="+ the_tag +"&result_type=recent&count=" + str(init_size))
		results.extend(onecall)
		print(onecall)
		if len(onecall) > 1:
			max_id = onecall[len(onecall) - 1].AsDict()["id"]
			max_date = onecall[len(onecall) - 1].AsDict()["created_at"]
		while len(results) < size and len(onecall) > 1:
			print("Scrolling")
			print(max_id)
			print(max_date)
			print(len(onecall))
			onecall = tg.api.GetSearch(raw_query="q="+ the_tag +"&result_type=recent&count=" + str(init_size) + "&max_id=" + str(max_id))
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
			with open("data/" + htag.replace("/", "-") + ".json", "w") as f:
				json.dump(res, f)
			#json.dump(res, "data/" + htag + ".json")
		return 
	def get_user(self, user):
		return -1
	def get_users_posts(self, users):
		return -1
	def get_users_followers(self, users, wfile=None):
		dumpobj = {}
		for user in users:
			results = self.get_followers_list(user)
			print(len(results))
			dumpobj[user] = results
		if wfile is not None:
			with open("data/users/" + wfile + ".json", "w") as f:
				json.dump(dumpobj, f)
			return
		else:
			return dumpobj
	def get_followers_list(self, user):
		results = []
		
		onecall = self.api.GetFollowerIDsPaged(screen_name=user)
		results.extend(list(map(lambda x: x ,onecall[2])))
		
		max_id = onecall[0]
		while len(onecall[2]) > 1:
			print("Scrolling")
			print(len(onecall[2]))
			onecall = self.api.GetFollowerIDsPaged(screen_name=user, cursor=max_id)
			results.extend(list(map(lambda x: x, onecall[2])))
			max_id = onecall[0]

		return results

	def get_friends_from_users_file(self, rfile, wfile=None):
		print("GETTING FRIENDS")
		rf = open("data/users/" + rfile + ".json")
		usersdata = json.load(rf)
		results = {}
		for x in usersdata:
			print(x)
			#results[x] = self.get_friends_list(x, user_id_flag=False)
			results[x] = {}
			for u in usersdata[x]:
				print(u)
				try:
					results[x][u] = self.get_friends_list(u)
				except:
					print("passing")
					continue

		if wfile is not None:
			with open("data/users/" + wfile + ".json", "w") as f:
				json.dump(results, f)
			return
		else:
			return results


	def get_friends_list(self, user, user_id_flag=True):
		results = []
		if user_id_flag:
			onecall = self.api.GetFriendIDsPaged(user_id=user)
		else:
			onecall = self.api.GetFriendIDsPaged(screen_name=user)
		results.extend(list(map(lambda x: x ,onecall[2])))
		
		max_id = onecall[0]
		while len(onecall[2]) > 1:
			print("Scrolling")
			print(len(onecall[2]))
			if user_id_flag:
				onecall = self.api.GetFriendIDsPaged(user_id=user, cursor=max_id)
			else:
				onecall = self.api.GetFriendIDsPaged(screen_name=user, cursor=max_id)
			results.extend(list(map(lambda x: x, onecall[2])))
			max_id = onecall[0]

		return results



def combine_json(json_names):
	bigjson = []
	for htag in json_names:
		with open("data/" + htag + ".json", "r") as f:
			hdata = json.load(f)
			bigjson.extend(hdata)
		print(len(bigjson))

	with open("data/" + "all_blogs_and_hashtags" + ".json", "w") as wf:
		json.dump(bigjson, wf)


def get_intersections(rfile, wfile, twitterthing):
	f = open("data/users/" + rfile + ".json", "r")
	d = json.load(f)
	thing = 1
	nodes = {}
	links = {}

	intersect_results = {"nodes" :[], "links" : []}
	for uname in d:
		nodes[uname] = 0
		for user_id_1 in d[uname]:
			print(len(d[uname][user_id_1]))
			for user_id_2 in d[uname]:
				if user_id_1 == user_id_2:
					thing = 1
				elif user_id_1 is uname or user_id_2 is uname:
					thing = 2
				else:
					set_result = set.intersection(set(d[uname][user_id_1]), set(d[uname][user_id_2]))
					for matched_id in set_result:
						sname = twitterthing.api.GetUser(matched_id).screen_name
						if sname == uname:
							thing = 2
						else:
							linkname = sname + ":" + uname
							nodes[uname] += 1
							if sname in nodes:
								nodes[sname] += 1
								links[linkname] += 1
							else:
								nodes[sname] = 1
								links[linkname] = 1

	intersect_results["nodes"] = list(map(lambda x: { "id" : x, "score" : nodes[x] }, nodes.keys()))
	intersect_results["links"] = list(map(lambda x: { "source" : x.split(":")[0], "target" : x.split(":")[1], "weight" : links[x] }, links.keys()))
	wf = open("data/users/" + wfile + ".json", "w")
	json.dump(intersect_results, wf, indent=4)
				
	return
if __name__ == "__main__":

	cleaned_blogs = ["messageboards.webmd.com/family-pregnancy",
	"embracerace.org",
	"sallyclarkson.com/blog",
	"cincinnatiparent.com",
	"babycenter.com",
	"parents.com",
	"parenting.com",
	"verywellfamily.com",
	"kellymom.com",
	"whattoexpect.com",
	"ahaparenting.com",
	"mother.ly",
	"workingmother.com",
	"mothersesquire.com",
	"themilitarywifeandmom.com",
	"babycenter.com",
	"whattoexpect.com",
	"lucieslist.com",
	"pregnantchicken.com",
	"mother.ly",
	"modernparentsmessykids.com",
	"busytoddler.com"]

	h_keywords = ['ACEs', 'traumainformed', 'ACEaware', 'AdverseChildhoodExperiences','TraumaResponsive','Resilience']
	u_keywords = ['ACEsConnection','DrBurkeHarris','CYWSanFrancisco','DocResilience','TreatingTrauma1','Reattachparent','ACEsAware','nctsn','CenterOnTrauma']

	#tg = TwitterGetter(TOKENS)
	#tg.get_hashtags(cleaned_blogs, size=1000)
	#print(tg.get_hashtag("parents.com", size=100))
	#print(tg.api.GetFriendIDs('DocResilience'))
	#cleaned_blogs_fnames = []
	#for htag in cleaned_blogs:
	#	cleaned_blogs_fnames.append(htag.replace("/", "-"))
	all_all = ["all_blog_tags", "all_htags"]
	combine_json(all_all)
	#tg.get_users_followers(['DocResilience'], wfile="all_users")
	#tg.get_friends_from_users_file('all_users', wfile='all_friends')
	#get_intersections("all_friends", "all_intersects", tg)


