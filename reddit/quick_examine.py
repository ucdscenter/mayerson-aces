import pandas
import matplotlib.pyplot as plt
import json

f = open("Parenting_2019-07", "r")
d = []
while 1:

	line = f.readline()
	if not line:
		break
	thing = json.loads(line)
	d.append(
		{"text_length" : len(thing['body'].split(" ")), 
		'date' : thing['created_utc']
		}
	)

da = pandas.DataFrame(data=d)
df = da[da['text_length'] > 65]
print(df.shape)
print(df['text_length'].mean())
print(df['text_length'].median())
print(df['text_length'].stdev())
#print(len(d))