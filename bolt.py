from core.colors import green, yellow, end, run, good, info, bad, white, red

lightning = '\033[93;5m⚡\033[0m'


def banner():
    print ('''
     %s⚡ %sBOLT%s  ⚡%s
    ''' % (yellow, white, yellow, end))


banner()

try:
    import concurrent.futures
    from pathlib import Path
except:
    print ('%s Bolt is not compatible with python 2. Please run it with python 3.' % bad)

try:
    from fuzzywuzzy import fuzz, process
except:
    import os
    print ('%s fuzzywuzzy library is not installed, installing now.' % info)
    os.system('pip3 install fuzzywuzzy')
    print ('%s fuzzywuzzy has been installed, please restart Bolt.' % info)
    quit()

import argparse
import json
import random
import re
import statistics

from core.entropy import isRandom
from core.datanize import datanize
from core.prompt import prompt
from core.photon import photon
from core.tweaker import tweaker
from core.evaluate import evaluate
from core.ranger import ranger
from core.zetanize import zetanize
from core.requester import requester
from core.utils import extractHeaders, strength, isProtected, stringToBinary, longestCommonSubstring

parser = argparse.ArgumentParser()
parser.add_argument('-u', help='target url', dest='target')
parser.add_argument('-t', help='number of threads', dest='threads', type=int)
parser.add_argument('-l', help='levels to crawl', dest='level', type=int)
parser.add_argument('--delay', help='delay between requests',
                    dest='delay', type=int)
parser.add_argument('--timeout', help='http request timeout',
                    dest='timeout', type=int)
parser.add_argument('--headers', help='http headers',
                    dest='add_headers', nargs='?', const=True)
args = parser.parse_args()

if not args.target:
    print('\n' + parser.format_help().lower())
    quit()

if type(args.add_headers) == bool:
    headers = extractHeaders(prompt())
elif type(args.add_headers) == str:
    headers = extractHeaders(args.add_headers)
else:
    from core.config import headers

target = args.target
delay = args.delay or 0
level = args.level or 2
timeout = args.timeout or 20
threadCount = args.threads or 2

allTokens = []
weakTokens = []
tokenDatabase = []
insecureForms = []

print (' %s Phase: Crawling %s[%s1/6%s]%s' %
       (lightning, green, end, green, end))
dataset = photon(target, headers, level, threadCount)
allForms = dataset[0]
print ('\r%s Crawled %i URL(s) and found %i form(s).%-10s' %
       (info, dataset[1], len(allForms), ' '))
print (' %s Phase: Evaluating %s[%s2/6%s]%s' %
       (lightning, green, end, green, end))

evaluate(allForms, weakTokens, tokenDatabase, allTokens, insecureForms)

if weakTokens:
    print ('%s Weak token(s) found' % good)
    for weakToken in weakTokens:
        url = list(weakToken.keys())[0]
        token = list(weakToken.values())[0]
        print ('%s %s %s' % (info, url, token))

if insecureForms:
    print ('%s Insecure form(s) found' % good)
    for insecureForm in insecureForms:
        url = list(insecureForm.keys())[0]
        action = list(insecureForm.values())[0]['action']
        form = action.replace(target, '')
        if form:
            print ('%s %s %s[%s%s%s]%s' %
                   (bad, url, green, end, form, green, end))

print (' %s Phase: Comparing %s[%s3/6%s]%s' %
       (lightning, green, end, green, end))
uniqueTokens = set(allTokens)
if len(uniqueTokens) < len(allTokens):
    print ('%s Potential Replay Attack condition found' % good)
    print ('%s Verifying and looking for the cause' % run)
    replay = False
    for each in tokenDatabase:
        url, token = next(iter(each.keys())), next(iter(each.values()))
        for each2 in tokenDatabase:
            url2, token2 = next(iter(each2.keys())), next(iter(each2.values()))
            if token == token2 and url != url2:
                print ('%s The same token was used on %s%s%s and %s%s%s' %
                       (good, green, url, end, green, url2, end))
                replay = True
    if not replay:
        print ('%s Further investigation shows that it was a false positive.')

p = Path(__file__).parent.joinpath('db/hashes.json')
with p.open('r') as f:
    hashPatterns = json.load(f)

if not allTokens:
    print ('%s No CSRF protection to test' % bad)
    quit()

aToken = allTokens[0]
matches = []
for element in hashPatterns:
    pattern = element['regex']
    if re.match(pattern, aToken):
        for name in element['matches']:
            matches.append(name)
if matches:
    print ('%s Token matches the pattern of following hash type(s):' % info)
    for name in matches:
        print ('    %s>%s %s' % (yellow, end, name))


def fuzzy(tokens):
    averages = []
    for token in tokens:
        sameTokenRemoved = False
        result = process.extract(token, tokens, scorer=fuzz.partial_ratio)
        scores = []
        for each in result:
            score = each[1]
            if score == 100 and not sameTokenRemoved:
                sameTokenRemoved = True
                continue
            scores.append(score)
        average = statistics.mean(scores)
        averages.append(average)
    return statistics.mean(averages)


try:
    similarity = fuzzy(allTokens)
    print ('%s Tokens are %s%i%%%s similar to each other on an average' %
           (info, green, similarity, end))
except statistics.StatisticsError:
    print ('%s No CSRF protection to test' % bad)
    quit()


def staticParts(allTokens):
    strings = list(set(allTokens.copy()))
    commonSubstrings = {}
    for theString in strings:
        strings.remove(theString)
        for string in strings:
            commonSubstring = longestCommonSubstring(theString, string)
            if commonSubstring not in commonSubstrings:
                commonSubstrings[commonSubstring] = []
            if len(commonSubstring) > 2:
                if theString not in commonSubstrings[commonSubstring]:
                    commonSubstrings[commonSubstring].append(theString)
                if string not in commonSubstrings[commonSubstring]:
                    commonSubstrings[commonSubstring].append(string)
    return commonSubstrings


result = {k: v for k, v in staticParts(allTokens).items() if v}

if result:
    print ('%s Common substring found' % info)
    print (json.dumps(result, indent=4))

simTokens = []

print (' %s Phase: Observing %s[%s4/6%s]%s' %
       (lightning, green, end, green, end))
print ('%s 100 simultaneous requests are being made, please wait.' % info)


def extractForms(url):
    response = requester(url, {}, headers, True, 0).text
    forms = zetanize(url, response)
    for each in forms.values():
        localTokens = set()
        inputs = each['inputs']
        for inp in inputs:
            value = inp['value']
            if value and re.match(r'^[\w\-_]+$', value):
                if strength(value) > 10:
                    simTokens.append(value)


while True:
    sample = random.choice(tokenDatabase)
    goodToken = list(sample.values())[0]
    if len(goodToken) > 0:
        goodCandidate = list(sample.keys())[0]
        break

threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=30)
futures = (threadpool.submit(extractForms, goodCandidate)
           for goodCandidate in [goodCandidate] * 30)
for i in concurrent.futures.as_completed(futures):
    pass

if simTokens:
    if len(set(simTokens)) < len(simTokens):
        print ('%s Same tokens were issued for simultaneous requests.' % good)
    else:
        print (simTokens)
else:
    print ('%s Different tokens were issued for simultaneous requests.' % info)

print (' %s Phase: Testing %s[%s5/6%s]%s' %
       (lightning, green, end, green, end))

parsed = ''
found = False
print ('%s Finding a suitable form for further testing. It may take a while.' % run)
for form_dict in allForms:
    for url, forms in form_dict.items():
        parsed = datanize(forms, tolerate=True)
        if parsed:
            found = True
            break
    if found:
        break

if not parsed:
    quit('%s No suitable form found for testing.' % bad)

origGET = parsed[0]
origUrl = parsed[1]
origData = parsed[2]

print ('%s Making a request with CSRF token for comparison.' % run)
response = requester(origUrl, origData, headers, origGET, 0)
originalCode = response.status_code
originalLength = len(response.text)
print ('%s Status Code: %s' % (info, originalCode))
print ('%s Content Length: %i' % (info, originalLength))
print ('%s Checking if the resonse is dynamic.' % run)
response = requester(origUrl, origData, headers, origGET, 0)
secondLength = len(response.text)
if originalLength != secondLength:
    print ('%s Response is dynamic.' % info)
    tolerableDifference = abs(originalLength - secondLength)
else:
    print ('%s Response isn\'t dynamic.' % info)
    tolerableDifference = 0

print ('%s Emulating a mobile browser' % run)
print ('%s Making a request with mobile browser' % run)
headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows CE; PPC; 240x320)'
response = requester(origUrl, {}, headers, True, 0).text
parsed = zetanize(origUrl, response)
if isProtected(parsed):
    print ('%s CSRF protection is enabled for mobile browsers as well.' % bad)
else:
    print ('%s CSRF protection isn\'t enabled for mobile browsers.' % good)

print ('%s Making a request without CSRF token parameter.' % run)

data = tweaker(origData, 'remove')
response = requester(origUrl, data, headers, origGET, 0)
if response.status_code == originalCode:
    if str(originalCode)[0] in ['4', '5']:
        print ('%s It didn\'t work' % bad)
    else:
        difference = abs(originalLength - len(response.text))
        if difference <= tolerableDifference:
            print ('%s It worked!' % good)
else:
    print ('%s It didn\'t work' % bad)

print ('%s Making a request without CSRF token parameter value.' % run)
data = tweaker(origData, 'clear')

response = requester(origUrl, data, headers, origGET, 0)
if response.status_code == originalCode:
    if str(originalCode)[0] in ['4', '5']:
        print ('%s It didn\'t work' % bad)
    else:
        difference = abs(originalLength - len(response.text))
        if difference <= tolerableDifference:
            print ('%s It worked!' % good)
else:
    print ('%s It didn\'t work' % bad)


seeds = ranger(allTokens)

print ('%s Checking if tokens are checked to a specific length' % run)

for index in range(len(allTokens[0])):
    data = tweaker(origData, 'replace', index=index, seeds=seeds)
    response = requester(origUrl, data, headers, origGET, 0)
    if response.status_code == originalCode:
        if str(originalCode)[0] in ['4', '5']:
            break
        else:
            difference = abs(originalLength - len(response.text))
            if difference <= tolerableDifference:
                print ('%s Last %i chars of token aren\'t being checked' %
                       (good, index + 1))
    else:
        break

print ('%s Generating a fake token.' % run)

data = tweaker(origData, 'generate', seeds=seeds)
print ('%s Making a request with the self generated token.' % run)

response = requester(origUrl, data, headers, origGET, 0)
if response.status_code == originalCode:
    if str(originalCode)[0] in ['4', '5']:
        print ('%s It didn\'t work' % bad)
    else:
        difference = abs(originalLength - len(response.text))
        if difference <= tolerableDifference:
            print ('%s It worked!' % good)
else:
    print ('%s It didn\'t work' % bad)

print (' %s Phase: Analysing %s[%s6/6%s]%s' %
       (lightning, green, end, green, end))

binary = stringToBinary(''.join(allTokens))
result = isRandom(binary)
for name, result in result.items():
    if not result:
        print ('%s %s : %s%s%s' % (good, name, green, 'non-random', end))
    else:
        print ('%s %s : %s%s%s' % (bad, name, red, 'random', end))
