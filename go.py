import json
import random, requests

primes = []

with open('100kprimes.txt', 'r') as primefile:
	for line in primefile:
		primes.append(int(line))

with open("stops.txt", 'r') as stops:
	data = json.load(stops)
	orgstops = data['data']['stops']

class Station():
	def __init__(self, primeid, name, orgid, lat, lon):
		self.primeid = primeid
		self.name = name
		self.orgid = orgid
		self.lat = lat
		self.lon = lon


def run_query(query):
    headers = {'Content-type': 'application/json'}
    
    r = requests.post("https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql", 
                  json={'query': query}, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


hslidToStopObject={}
nameToPrime={}
for stop in orgstops:
	if stop['name'] not in nameToPrime:
		nameToPrime[stop['name']] = primes.pop(0)
		
	newStation = Station(nameToPrime[stop['name']],stop['name'], stop['gtfsId'], stop['lat'], stop['lon']) 
	hslidToStopObject[newStation.orgid] = newStation
	print('{}, {}, {}, {}, {}'.format(newStation.name, newStation.primeid, newStation.orgid, newStation.lat, newStation.lon))

def getLine(number):
    query_stops_by_bus = '{routes(name: "' + str(number) + '" transportModes: BUS) \{shortName longName stops \{name gtfsId \}\}\}'
    result = run_query(query_stops_by_bus)
    route = result['data']['routes'][0]['stops']
    lineno = 1
    linetext = ""
    for stop in route:
        lineno *= nameToPrime[stop['name']]
        linetext += stop['name'] + "(" + str(nameToPrime[stop['name']]) +") -> "
    print('\n')
    print("Bus line: {}".format(lineno))
    print('\n')
    print (linetext)

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