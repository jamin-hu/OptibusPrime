emojiBase = {}

def emojify():
	with open("emoji-data.txt", 'r') as emojifile:
		counter = 0
		for line in emojifile:
			splitLine = line.split(')')
			emoji = splitLine[0].split('(')
			emojiBase[counter] = emoji[1].strip()
			print('{}, {}'.format(counter, emojiBase[counter]))
			counter = counter + 1

def safeEmojiLookup():
	file = open("emojilookup.txt", "x")
	counter = 0
	for x in range(0, len(emojiBase)):
		file.write('{}, {}\n'.format(x, emojiBase[x]))
	file.close()

def convertToBase(number, base):
	if number < base:
		return emojiBase[number]
	else:
		return convertToBase(number//base, base) + emojiBase[number%base]


emojify()
safeEmojiLookup()

#emojiList = []
print("aalto university: " + convertToBase(32771, len(emojiBase)))
print("senate square: " + convertToBase(1471, len(emojiBase)))
print("teekkarikyla: " + convertToBase(167, len(emojiBase)))
print("kamppi: " + convertToBase(23677, len(emojiBase)))
