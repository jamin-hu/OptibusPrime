#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 21:35:20 2019

@author: erich
"""

import requests

headers = {'Content-type': 'application/json'}

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

r = requests.post("https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql", 
                  json={'query': query_stops_by_bus}, headers=headers)

print(r.status_code, r.reason)
print(r.json())
#print(r.text[:300] + '...')
