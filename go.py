import json
import random, requests
from pprint import pprint

primes = []

with open('100kprimes.txt', 'r') as primefile:
	for line in primefile:
		primes.append(int(line))

emojilut = []
with open('emojilut.txt', 'r') as emojifile:
	for line in emojifile:
		emojilut.append(line[0])

with open("stops.txt", 'r') as stops:
	data = json.load(stops)
	orgstops = data['data']['stops']

class Station():
	def __init__(self, primeid, name, orgid, lat, lon, emojicode):
		self.primeid = primeid
		self.name = name
		self.orgid = orgid
		self.lat = lat
		self.lon = lon
		self.emojicode = emojicode

def emoji():
	with open("emoji-data.txt", 'r') as emojifile:
		counter = 0
		for line in emojifile:
			splitLine = line.split(')')
			emoji = splitLine[0].split('(')
			emojiBase[counter] = emoji[1].strip()
			print('{}, {}'.format(counter, emojiBase[counter]))
			counter = counter + 1

def convertToBase(number, base):
	if number < base:
		return emojiBase[number]
	else:
		return convertToBase(number//base, base) + emojiBase[number%base]


def run_query(query):
    headers = {'Content-type': 'application/json'}
    
    r = requests.post("https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql", 
                  json={'query': query}, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def address_search_to_lat_lon(text):    
    r = requests.get(
    'https://api.digitransit.fi/geocoding/v1/search',
    params={'text': text,
            'size': 1},
    )
    
    if r.status_code == 200:
        lon, lat = r.json()['features'][0]['geometry']['coordinates']
        print(text, "-> lat, lon: ", lat, lon)
        return lat, lon
    else:
        raise Exception("Query failed to run by address searching of {}. {}".format(r.status_code, text))

query_suggest_routes_p1 = """
{
  plan(
"""
query_suggest_routes_p2 = "    from: {{lat: {}, lon: {}}} \n"
query_suggest_routes_p3 = "    to: {{lat: {}, lon: {}}} \n"

query_suggest_routes_p4 = """

  ) {
    itineraries{
      legs {
        mode
        route {
          patterns {
            code
          }
        },
        from {
          stop{
            name
            gtfsId
          }
        },
        to {
          stop{
            name
            gtfsId
          }
        }
      }
    }
  }
}
"""

def gen_suggested_routes_in_codes(from_station_name, to_station_name):
    from_lat, from_lon = address_search_to_lat_lon(from_station_name)
    to_lat, to_lon = address_search_to_lat_lon(to_station_name)
    
#    query_suggest_routes = query_suggest_routes_p1 + \
#                           "    from: {lat: 60.170203, lon: 24.941074} \n" + \
#                           "    to: {lat: 60.185052, lon: 24.825671} \n" + \
#                           query_suggest_routes_p4
                           
    query_suggest_routes = query_suggest_routes_p1 + \
                           query_suggest_routes_p2.format(from_lat, from_lon) + \
                           query_suggest_routes_p3.format(to_lat, to_lon) + \
                           query_suggest_routes_p4
    
    
    itns_pattern_codes = []
    
    itns = run_query(query_suggest_routes)
    
    for i, itn in enumerate(itns['data']['plan']['itineraries']):
        #print("itinerary: ", i)
        # print(itn)
        itn_pattern_codes = []
        for item in itn['legs']:
            #print(item)
            if item['mode'] != 'WALK':
                # get the route -> patterns -> code
                pattern_codes = [ d['code']for d in item['route']['patterns'] ]
                #print(pattern_codes)
                print(item)
                itn_pattern_codes.append(pattern_codes)
        itns_pattern_codes.append(itn_pattern_codes)
    
    return itns_pattern_codes[0][0]


hslidToStopObject={}
nameToPrime={}
emojiBase = {}

emoji()

for stop in orgstops:
	if stop['name'] not in nameToPrime:
		nameToPrime[stop['name']] = primes.pop(0)
	emojicode = convertToBase(nameToPrime[stop['name']], len(emojiBase))	
	newStation = Station(nameToPrime[stop['name']],stop['name'], stop['gtfsId'], stop['lat'], stop['lon'], emojicode) 
	hslidToStopObject[newStation.orgid] = newStation
	print('{}, {}, {}, {}, {}, {}'.format(newStation.name, newStation.primeid, newStation.orgid, newStation.lat, newStation.lon, newStation.emojicode))

print('\nAll stops created.\n')

def getLine(number):
    query_stops_by_bus = '{routes(name: "' + str(number) + '" ) \{shortName longName patterns \{code directionId name stops \{name gtfsId \}\}\}\}'
    result = run_query(query_stops_by_bus)
    orgRouteName = result['data']['routes'][0]['patterns'][0]['name']
    route = result['data']['routes'][0]['patterns'][0]['stops']
    lineno = 1
    linetext = ""
    for stop in route:
        lineno *= nameToPrime[stop['name']]
        linetext += stop['name'] + "(" + str(nameToPrime[stop['name']]) +") -> "
    print('\n')
    print("Lame original name that isn't helpful: {}".format(orgRouteName))
    print("Bus line: {}".format(lineno))
    print('\n')
    print (linetext)

def getl(code):
    query_stops_by_bus = '{pattern(id: "' + str(code) + '" ) \{name stops \{name gtfsId \}\}\}'
    result = run_query(query_stops_by_bus)
    print (result)
    orgRouteName = result['data']['pattern']['name']
    route = result['data']['pattern']['stops']
    lineno = 1
    linetext = ""
    for stop in route:
        lineno *= nameToPrime[stop['name']]
        linetext += stop['name'] + "(" + str(nameToPrime[stop['name']]) +") -> "
    print('\n')
    print("Lame original name that isn't helpful: {}".format(orgRouteName))
    print("Bus line: {}".format(lineno))
    print('\n')
    print (linetext)

def planRoute(from_station_name, to_station_name):
	route = gen_suggested_routes_in_codes(from_station_name, to_station_name)
	for branch in route:
		print('\n\n\n')
		line = branch[0][0]
		print(line)

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

# results = gen_suggested_routes_in_codes('city center', 'aalto university')
# for i, result in enumerate(results):
#     print(f"itinerary [{i}]: {result[0][0]}")
#     getl(result[0][0])

planRoute('city center', 'Vanhan-Mankkaan tie 35')