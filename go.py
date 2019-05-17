import json

with open("stops.txt", 'r') as stops:
	data = json.load(stops)
	stops = data['data']['stops']

for stop in stops:
	name = stop['name']
	orgid = stop['gtfsId']
	print('{}, {}'.format(name, orgid))