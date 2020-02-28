from .abstract_command import AbstractCommand


class DeployConfig(AbstractCommand):
    def get_name(self):
        return "deploy"

    def get_description(self):
        return "Deploy a config"

    def get_options(self):
        return [{"name": "index_name",
                 "description": "name of the config to deploy"}]

    def run(self, args):
        if len(args) <= 0:
            print(
                'You can only deploy one config at a time, index_name missing. Aborting')
            exit(1)
        else:
            from deployer.src.index import deploy_config
            deploy_config(args[0])
