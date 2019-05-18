import json

primes = []

with open('100kprimes.txt', 'r') as primefile:
	for line in primefile:
		primes.append(int(line))

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


