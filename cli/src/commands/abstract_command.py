from os import environ


class AbstractCommand:
    def run(self, args):
        raise Exception("run need to be implemented")

    def get_name(self):
        raise Exception("get_name need to be implemented")

    def get_description(self):
        raise Exception("get_description need to be implemented")

    def get_usage(self):
        return "  ./docsearch " + self.get_name()

    def get_options(self):
        return []

    def nb_options(self):
        return len(list(
            [x for x in self.get_options() if x.get("optional") is None]))

    def get_option(self, name, args):
        options = self.get_options()
        index = [i for i, j in enumerate(options) if j["name"] == name]
        if len(index) == 0:
            return None
        else:
            index = index[0]

        if index < len(args):
            return args[index]
        else:
            return options[index]["optional"]

    def check_docsearch_app_id(self, action_description):
        if environ.get("APPLICATION_ID") != "BH4D9OD16A":
            print("The APP_ID is not BH4D9OD16A. You can not " + action_description +
                  " if you are not using the docsearch account")
            exit(1)

    def check_not_docsearch_app_id(self, action_description):
        if environ.get("APPLICATION_ID") == "BH4D9OD16A":
            print("The APP_ID is BH4D9OD16A. You can not " + action_description +
                  " if you are using the docsearch account")
            exit(1)

    @staticmethod
    def exec_shell_command(arguments, env=None):
        if env is None:
            env = {}
        merge_env = environ.copy()
        merge_env.update(env)

        from subprocess import Popen
        p = Popen(arguments, env=merge_env)
        try:
            p.wait()
        except KeyboardInterrupt:
            p.kill()
            p.wait()
            p.returncode = 1

        return p.returncode
