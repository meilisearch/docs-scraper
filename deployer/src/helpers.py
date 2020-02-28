import os

api_key_prod = os.environ.get('API_KEY_PROD', '')

slack_hook = os.environ.get('SLACK_HOOK', '')


def confirm(message="Confirm"):
    from builtins import input

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


def get_user_value(message):
    from builtins import input

    prompt = message
    return input(prompt)


def make_custom_get_request(url):
    import requests

    return requests.get(url)


def make_request(endpoint, type=None, data=None, username=None, password=None,
                 json_request=False):
    import requests

    if "://" not in endpoint:
        print("Wrong endpoint:{}, it should be a complete URL".format(endpoint))
        exit(6)

    if username is None or password is None:
        print("{}: both username and password must be set".format(endpoint))
        exit(7)

    success_codes = [200, 201, 204]

    if data and not isinstance(data, dict):
        raise ValueError(data + " must be a dict ")

    if type == 'POST':
        if json_request:
            r = requests.post(endpoint,
                              auth=(username, password),
                              json=data)
        else:
            r = requests.post(endpoint,
                              auth=(username, password),
                              data=data)

        if r.status_code // 100 != 2:
            print('ISSUE for POST request : {} with params: {}'.format(endpoint,
                data))
            print(r.text)
        return r

    if type == 'DELETE':
        r = requests.delete(endpoint,
                            auth=(username, password))

        if r.status_code not in success_codes:
            print('ISSUE for DELETE request : {} with params: {}'.format(endpoint,
                                                                       data))
        return r

    if type == 'PUT':
        r = requests.put(endpoint,
                         auth=(username, password),
                         data=data)
        print(r.status_code)
        if r.status_code // 100 != 2:
            print('ISSUE for PUT request : {} with params: {}'.format(endpoint,
                data))
        return r

    if data != None:
        r = requests.get(endpoint,
                         auth=(username, password),
                         params=data)
    else:
        r = requests.get(endpoint,
                         auth=(username, password))

    if r.status_code // 100 != 2:
        print('ISSUE for GET request : {} with params: {}'.format(endpoint, data))

    if json_request:
        r.json()

    return r.text


def send_slack_notif(reports):
    if slack_hook == '':
        raise ValueError("NO SLACK_HOOK")

    from slacker import Slacker

    slack = Slacker(None, slack_hook)

    slack.incomingwebhook.post({
        "text": "",
        "channel": "#notif-docsearch",
        "username": "Deployer",
        "icon_emoji": ":rocket:",
        "attachments": reports
    })


def check_output_decoded(command, cwd=None):
    from subprocess import check_output
    return check_output(command, cwd=cwd).decode()
