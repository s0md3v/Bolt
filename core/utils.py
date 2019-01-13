import re
import math
from modules.erfc import erfc
from core.config import token

def monobit(string):
    string = ''.join(format(ord(x), 'b') for x in string)
    count = 0
    for char in string:
        if char == '0':
            count -= 1
        else:
            count += 1
    value = erfc(math.fabs((count / math.sqrt(len(string)))) / math.sqrt(2))
    return value

def entropy(string):
    digits = re.findall(r'\d', string)
    lowerAlphas = re.findall(r'[a-z]', string)
    upperAlphas = re.findall(r'[A-Z]', string)
    entropy = len(set(digits + lowerAlphas + upperAlphas))
    if not digits:
        entropy = entropy/2
    return entropy

def isProtected(parsed):
    protected = False
    parsedForms = list(parsed.values())
    for oneForm in parsedForms:
        inputs = oneForm['inputs']
        for inp in inputs:
            name = inp['name']
            kind = inp['type']
            value = inp['value']
            if re.match(token, value):
                protected = True
    return protected

def extractHeaders(headers):
    sorted_headers = {}
    matches = re.findall(r'(.*):\s(.*)', headers)
    for match in matches:
        header = match[0]
        value = match[1]
        try:
            if value[-1] == ',':
                value = value[:-1]
            sorted_headers[header] = value
        except IndexError:
            pass
    return sorted_headers

def getUrl(url, data, GET):
    if GET:
        return url.split('?')[0]
    else:
        return url

def getParams(url, data, GET):
    params = {}
    if GET:
        if '=' in url:
            data = url.split('?')[1]
            if data[:1] == '?':
                data = data[1:]
        else:
            data = ''
    parts = data.split('&')
    for part in parts:
        each = part.split('=')
        try:
            params[each[0]] = each[1]
        except IndexError:
            params = None
    return params