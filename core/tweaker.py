from core.config import tokenPattern
import random
import re


def tweaker(data, strategy, index=0, seeds=[None, None]):
    digits = seeds[0]
    alphabets = seeds[1]
    newData = {}
    if strategy == 'clear':
        for name, value in data.items():
            if re.match(tokenPattern, value):
                value = ''
            newData[name] = value
        return newData
    elif strategy == 'remove':
        for name, value in data.items():
            if not re.match(tokenPattern, value):
                newData[name] = value
    elif strategy == 'break':
        for name, value in data.items():
            if re.match(tokenPattern, value):
                value = value[:index]
                for i in index:
                    value += random.choice(digits + alphabets)
            newData[name] = value
    elif strategy == 'generate':
        for name, value in data.items():
            if re.match(tokenPattern, value):
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
    elif strategy == 'replace':
        for name, value in data.items():
            if re.match(tokenPattern, value):
                value
    return newData
