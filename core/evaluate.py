from re import match
from core.utils import strength
from core.config import commonNames


def evaluate(dataset, weakTokens, tokenDatabase, allTokens, insecureForms):
    done = []
    for i in dataset:
        for url, page in i.items():
            localTokens = set()
            for each in page.values():
                protected = False
                action = each['action']
                method = each['method']
                inputs = each['inputs']
                for inp in inputs:
                    name = inp['name']
                    value = inp['value']
                    if value and match(r'^[\w\-_]+$', value):
                        if strength(value) > 10:
                            localTokens.add(value)
                            protected = True
                            break
                        elif name.lower() in commonNames:
                            weakTokens.append({url: {name: value}})
                if not protected and action not in done:
                    done.append(done)
                    insecureForms.append({url: each})
            for token in localTokens:
                allTokens.append(token)
            tokenDatabase.append({url: localTokens})
