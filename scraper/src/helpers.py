from builtins import input
from cssselect import HTMLTranslator
import json


def confirm(message="Confirm"):
    prompt = message + ' [y/n]:\n'

    while True:
        ans = input(prompt)
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False


def css_to_xpath(css):
    return HTMLTranslator().css_to_xpath(css) if len(css) > 0 else ""


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def to_json(my_json):
    try:
        jsonized = json.loads(my_json)
    except ValueError:
        return None
    return jsonized
