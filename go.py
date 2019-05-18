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
			emojiBase.append( emoji[1].strip())
			print('{}, {}'.format(counter, emojiBase[counter]))
			counter = counter + 1

def convertToBase(number, base=1000):
	if number < base:
		return emojiBase[number]
	else:
		return convertToBase(number//base, base) + emojiBase[number%base]

def deemoji(emojistring):
	result = 0
	for emoji in emojistring:
		result *= 1000
		result += emojiBase.index(emoji)
	return result

def sumemoji(one, two):
	return convertToBase(deemoji(one) + deemoji(two))

def modemoji(one, two):
	return convertToBase(deemoji(one) % deemoji(two))

def divemoji(one, two):
	return convertToBase(int(deemoji(one) / deemoji(two)))

def mulemoji(one, two):
	return convertToBase(deemoji(one) * deemoji(two))

def subemoji(one, two):
	return convertToBase(deemoji(one) - deemoji(two))


def run_query(query):
    headers = {'Content-type': 'application/json'}
    
    r = requests.post("https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql", 
                  json={'query': query}, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(r.status_code, query))

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
        
        from {
          name
          stop{
            gtfsId
          }
        },
          
        route {
          patterns {
            code
          }
        },
          
        to {
          name
          stop{
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
                           
    query_suggest_routes = query_suggest_routes_p1 + \
                           query_suggest_routes_p2.format(from_lat, from_lon) + \
                           query_suggest_routes_p3.format(to_lat, to_lon) + \
                           query_suggest_routes_p4
    
    itns = []
    """    
    itns = [
            [[{mode: WALK}, {from:}, {to}], 
             [{mode: BUS}, {from:}, {to:}], 
             [{mode: WALK}, {from:}, {to:}]
            ], # itn
             
            [...], # itn
            ...,
           ]
    """
    
    query_results = run_query(query_suggest_routes)
    
    for i, query_result in enumerate(query_results['data']['plan']['itineraries']):
        itn = []
        #itn_pattern_codes = []
        for item in query_result['legs']:
            leg = {}
            leg['mode'] = item['mode']
            leg['from'] = item['from']['name']
            leg['to'] = item['to']['name']
            
            
            if item['mode'] != 'WALK':
                leg['from_stop_id'] = item['from']['stop']['gtfsId']
                leg['to_stop_id'] = item['to']['stop']['gtfsId']
                leg['1st_route_pattern_id'] = item['route']['patterns'][0]['code']
                leg['all route_pattern_ids'] = [ d['code']for d in item['route']['patterns'] ]
                
            
            itn.append(leg)
        itns.append(itn)
    
    return itns


hslidToStopObject={}
nameToPrime={}
emojiBase = []

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
    # print (result)
    orgRouteName = result['data']['pattern']['name']
    route = result['data']['pattern']['stops']
    lineno = 1
    linetext = ""
    for stop in route:
        lineno *= nameToPrime[stop['name']]
        linetext += stop['name'] + "(" + str(nameToPrime[stop['name']]) +") -> "
    return lineno


dec = 'dec'
emoji = 'emoji'

def planRoute(from_station_name, to_station_name, mode=dec):
	route = gen_suggested_routes_in_codes(from_station_name, to_station_name)[0]
	for step in route:
		if step['mode'] == 'WALK':
			continue
		print('\n')
		busline = getl(step['1st_route_pattern_id'])
		destination = nameToPrime[step['to']]
		if mode==emoji:
			busline = convertToBase(busline)
			destination = convertToBase(destination)
		print (f"take the {step['mode']} {busline}")
		print(f"to {destination} aka {step['to']}")
		# print (step)

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

# planRoute('city center', 'Vanhan-Mankkaan tie 35')
#planRoute('city center', 'heinjoenpolku 2')
# route = gen_suggested_routes_in_codes('city center', 'Vanhan-Mankkaan tie 35')
