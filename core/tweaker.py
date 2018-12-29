from core.config import token
import random
import re

def tweaker(data, strategy, index=0, seeds=[None, None]):
	newData = {}
	if strategy == 'clear':
		for name, value in data.items():
			if re.match(token, value):
				value = ''
			newData[name] = value
		return newData
	elif strategy == 'remove':
		for name, value in data.items():
			if not re.match(token, value):
				newData[name] = value
	elif strategy == 'break':
		for name, value in data.items():
			if re.match(token, value):
				value = value[:-index]
			newData[name] = value
	elif strategy == 'generate':
		digits = seeds[0]
		alphabets = seeds[1]
		for name, value in data.items():
			if re.match(token, value):
				newToken = ''
				for char in list(value):
					if char in digits:
						newToken += random.choice(digits)
					elif char in alphabets:
						newToken += random.choice(alphabets)
					else:
						newToken += char
				newData[name] = newToken
			else:
				newData[name] = value
	return newData