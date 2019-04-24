import random
import re

from core.config import password, email, tokenPattern, strings


def datanize(forms, tolerate=False):
    parsedForms = list(forms.values())
    for oneForm in parsedForms:
        data = {}
        login = False
        protected = False
        action = oneForm['action']
        method = oneForm['method']
        inputs = oneForm['inputs']
        for inp in inputs:
            name = inp['name']
            kind = inp['type']
            value = inp['value']
            if re.match(tokenPattern, value):
                protected = True
            if kind == 'password':
                data[name] = password
                login = True
            if kind == 'email':
                data[name] = email
            if kind == 'text':
                data[name] = random.choice(strings)
            else:
                data[name] = value
        if method == 'GET':
            GET = True
        else:
            GET = False
        if protected:
            if not login or tolerate:
                return [GET, action, data]
    return None
