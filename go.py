import json
import random
import requests

primes = []

with open('100kprimes.txt', 'r') as primefile:
	for line in primefile:
		primes.append(int(line))

with open("stops.txt", 'r') as stops:
	data = json.load(stops)
	orgstops = data['data']['stops']

class Station():
	def __init__(self, primeid, name, orgid):
		self.primeid = primeid
		self.name = name
		self.orgid = orgid

def run_query(query):
    headers = {'Content-type': 'application/json'}
    
    r = requests.post("https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql", 
                  json={'query': query}, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def getRoute(number):
    query_stops_by_bus = '{routes(name: "' + str(number) + '" transportModes: BUS) \{shortName longName stops \{name gtfsId \}\}\}'
    route = run_query(query_stops_by_bus)
    return route['data']['routes'][0]['stops']

stops=[]
for stop in orgstops:
	newStation = Station(primes.pop(0), stop['name'], stop['gtfsId']) 
	stops.append(newStation)
	print('{}, {}, {}'.format(newStation.name, newStation.primeid, newStation.orgid))


def makeLine(length):
	lineno = 1
	linetext = ""
	for a in range(0, length):
		stop = random.choice(stops)
		lineno *= stop.primeid
		linetext += stop.name + " -> "
	print("Line number: {}".format(lineno))
	print("Route:")
	print(linetext)