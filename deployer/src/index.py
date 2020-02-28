import sys
import os

from . import helpers
from .config_manager import ConfigManager
from . import fetchers


def print_init():
    if 'APPLICATION_ID' not in os.environ or 'API_KEY' not in os.environ:
        print("")
        print("ERROR: missing configuration")
        print("")
        sys.exit(1)

    print("\033[0m")
    print("")
    print("=======================")
    print("=  Deploy connectors  =")
    print("=======================")
    print("")


def deploy_config(config_name):
    from os import environ, path

    print_init()

    config_folder = environ.get('PUBLIC_CONFIG_FOLDER')

    if config_folder is None:
        print('PUBLIC_CONFIG_FOLDER must be defined in the environment')
        exit()

    config_folder += '/configs'

    if not path.isdir(config_folder):
        print("Folder: " + config_folder + " does not exist")
        exit()

    is_new_config = config_name in fetchers.get_configs_from_repos()

    # Not using the config manager to avoid it stashing the config that we want to push
    helpers.check_output_decoded(['git', 'add', config_name + '.json'],
                                 cwd=config_folder)
    helpers.check_output_decoded(
        ['git', 'commit', '-m', 'update ' + config_name],
        cwd=config_folder)
    config_manager = ConfigManager().instance

    helpers.check_output_decoded(['git', 'push', 'origin', 'master'],
                                 cwd=config_folder)

    # Already live, we will only update the change
    if is_new_config:
        deploy_configs([], [config_name], [], force_deploy=True)
    # Didn't exist, we add it
    else:
        deploy_configs([config_name], [], [], force_deploy=True)

    config_manager.destroy()


def deploy_configs(added, changed, removed, force_deploy=False):
    config_manager = ConfigManager().instance

    added_log = ""
    updated_log = ""
    removed_log = ""

    if len(added):
        print("")
        print("Will be \033[1;32madded\033[0m :")
        for config in added:
            added_log += " - " + config + "\n"
        print(added_log)

    if len(removed):
        print("")
        print("Will be \033[1;31mdeleted\033[0m :")
        for config in removed:
            removed_log += " - " + config + "\n"
        print(removed_log)

    if len(changed):
        print("")
        print("Will be \033[1;33mupdated\033[0m :")
        for config in changed:
            log = " - " + config
            cli_log = log
            updated_log += log + "\n"
            print(cli_log)

    print("")

    if len(added) or len(removed) > 0 or len(changed):
        if force_deploy or helpers.confirm() is True:
            reports = []

            if len(added):
                print("")
                for current_config_name in added:
                    config_manager.add_config(current_config_name)
                reports.append(
                    {'title': 'Added connectors', 'text': added_log})

            if len(changed):
                print("")

                for current_config_name in changed:
                    config_manager.update_config(current_config_name)
                reports.append({
                    'title': 'Updated connectors',
                    'text': updated_log
                })

            if len(removed):
                for current_config_name in removed:
                    config_manager.remove_config(current_config_name)

                reports.append({
                    'title': 'Removed connectors',
                    'text': removed_log
                })
            helpers.send_slack_notif(reports)

    else:
        print("Nothing to do")
