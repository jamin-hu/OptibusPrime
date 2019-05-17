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

def run_query(query):
    headers = {'Content-type': 'application/json'}
    
    r = requests.post("https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql", 
                  json={'query': query}, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


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


query_suggest_routes = """
{
  plan(
    fromPlace: "Kamppi, Helsinki::60.168992,24.932366",
    toPlace: "Pisa, Espoo::60.175294,24.684855",
  ) {
    itineraries{
      walkDistance,
      duration,
      legs {
        mode
        startTime
        endTime
        from {
          lat
          lon
          name
          stop {
            code
            name
          }
        },
        to {
          lat
          lon
          name
        },
        agency {
          gtfsId
	  name
        },
        distance
        legGeometry {
          length
          points
        }
      }
    }
  }
}
"""

def genSuggestedRoutes(from_station_name, to_station_name):
    pass

#print(run_query(query_stops_by_bus))
#print(run_query(query_all_stops_of_a_bus))
print(run_query(query_suggest_routes))