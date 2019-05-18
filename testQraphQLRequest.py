#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 21:35:20 2019

@author: erich

ref:
https://stackoverflow.com/questions/11322430/how-to-send-post-request
https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad
"""

import requests
import json
from pprint import pprint

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



query_stops_by_bus = """
{
  routes(name: "550", transportModes: BUS) {
    shortName
    longName
    patterns {
      code
      directionId
      name
`    }
  }
}
"""

query_all_stops_of_a_bus = """
{
  pattern(id: "HSL:2550:0:01") {
    name
    stops {
      name
    }
  }
}
"""


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
        #print(itn)
        itn_pattern_codes = []
        for item in itn['legs']:
            #print(item)
            if item['mode'] != 'WALK':
                # get the route -> patterns -> code
                pattern_codes = [ d['code']for d in item['route']['patterns'] ]
                #print(pattern_codes)
                itn_pattern_codes.append(pattern_codes)
        itns_pattern_codes.append(itn_pattern_codes)
    
    return itns_pattern_codes


results = gen_suggested_routes_in_codes('city center', 'aalto university')
for i, result in enumerate(results):
    print(f"itinerary [{i}]: {result}")
#pprint(itns)


#print(address_search_to_lat_lon('city center'))
#print(json.dumps(json.loads(addressSearch('kamppi')), \
#                 indent=4, sort_keys=True) )