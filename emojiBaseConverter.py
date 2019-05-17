emojiBase = {}

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


emoji()

#emojiList = []
print(convertToBase(32771, len(emojiBase)))