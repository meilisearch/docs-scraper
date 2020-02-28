from .abstract_command import AbstractCommand


class RunTests(AbstractCommand):
    def get_name(self):
        return "test"

    def get_description(self):
        return "Run tests"

    def get_options(self):
        return [{"name": "docker",
                 "description": "run test from docker image",
                 "optional": False}]

    @staticmethod
    def docker_parse(args):
        if len(args) < 2:
            return False
        if isinstance(args[1], bool):
            return args[1]
        if args[1] is "no_browser":
            return "no_browser"

        return isinstance(args[1], str) and args[1].lower() == "true"

    def run(self, args):
        docker = self.get_option("docker", args)
        if docker == True:
            self.exec_shell_command(["./docsearch", "docker:build", "true"])
            run_command = [
                "docker",
                "run",
                "--rm",
                "-i",
                "--name",
                "docsearch-scraper-test",
                "-t",
                "algolia/docsearch-scraper-test"]
            return self.exec_shell_command(run_command)
        test_command = ["pytest", "./scraper/src"]

        if docker == "no_browser":
            test_command.append("-k")
            test_command.append("not _browser")
        print(test_command)
        return self.exec_shell_command(test_command)
