import json
import random

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