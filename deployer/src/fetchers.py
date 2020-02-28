import os
import json
from collections import OrderedDict
from os import environ
from . import helpers


def get_configs_from_repos():
    configs = {}
    public_dir = environ.get('PUBLIC_CONFIG_FOLDER')
    private_dir = environ.get('PRIVATE_CONFIG_FOLDER')

    tracked_configs = helpers.check_output_decoded(
        ['git', 'ls-tree', '-r', 'master', '--name-only'],
        cwd=public_dir).splitlines()

    if public_dir is None or private_dir is None:
        print(
            'PUBLIC_CONFIG_FOLDER and PRIVATE_CONFIG_FOLDER must be defined in the environment')
        exit()

    for dir in [public_dir + '/configs', private_dir + '/configs']:
        for f in os.listdir(dir):
            path = dir + '/' + f

            if 'json' not in path:
                continue

            if os.path.isfile(path):
                with open(path, 'r') as f:
                    txt = f.read()
                config = json.loads(txt, object_pairs_hook=OrderedDict)
                if 'configs/{}.json'.format(
                        config['index_name']) in tracked_configs:
                    configs[config['index_name']] = config

    print('{} docs in public and private repo'.format(len(configs)))

    return configs
