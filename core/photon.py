# Let's import what we need
from re import findall
import concurrent.futures
from urllib.parse import urlparse  # for python3

from core.colors import run
from core.zetanize import zetanize
from core.requester import requester
from core.utils import getUrl, getParams, remove_file


def photon(seedUrl, headers, depth, threadCount):
    forms = []  # web forms
    processed = set()  # urls that have been crawled
    storage = set()  # urls that belong to the target i.e. in-scope
    scheme = urlparse(seedUrl).scheme
    host = urlparse(seedUrl).netloc
    main_url = scheme + '://' + host
    storage.add(seedUrl)

    def rec(url):
        processed.add(url)
        urlPrint = (url + (' ' * 60))[:60]
        print ('%s Parsing %-40s' % (run, urlPrint), end='\r')
        url = getUrl(url, '', True)
        params = getParams(url, '', True)
        if '=' in url:
            inps = []
            for name, value in params.items():
                inps.append({'name': name, 'value': value})
            forms.append(
                {url: {0: {'action': url, 'method': 'get', 'inputs': inps}}})
        response = requester(url, params, headers, True, 0).text
        forms.append({url: zetanize(url, response)})
        matches = findall(
            r'<[aA][^>]*?(href|HREF)=["\']{0,1}(.*?)["\']', response)
        for link in matches:  # iterate over the matches
            # remove everything after a "#" to deal with in-page anchors
            link = link[1].split('#')[0].lstrip(' ')
            if link[:4] == 'http':
                if link.startswith(main_url):
                    storage.add(link)
            elif link[:2] == '//':
                if link.split('/')[2].startswith(host):
                    storage.add(scheme + '://' + link)
            elif link[:1] == '/':
                storage.add(remove_file(url) + link)
            else:
                usable_url = remove_file(url)
                if usable_url.endswith('/'):
                    storage.add(usable_url + link)
                elif link.startswith('/'):
                    storage.add(usable_url + link)
                else:
                    storage.add(usable_url + '/' + link)
    for x in range(depth):
        urls = storage - processed
        threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        futures = (threadpool.submit(rec, url) for url in urls)
        for i in concurrent.futures.as_completed(futures):
            pass
    return [forms, len(processed)]
