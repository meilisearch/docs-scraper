from .abstract_command import AbstractCommand


class AbstractBuildDocker(AbstractCommand):
    @staticmethod
    def build_docker_file(file, image="algolia/docsearch-scraper-dev",
                          local_tag=False):
        tags = [image]

        if local_tag:
            tag = AbstractBuildDocker.get_local_tag().decode()
            tags.append(image + ":" + tag)

        cmd = ["docker", "build"] + [param for tag in tags for param in
                                     ['-t', tag]] + ["-f", file, "."]
        return AbstractCommand.exec_shell_command(cmd)

    def get_options(self):
        return [{"name": "local_tag",
                 "description": "tag image according to source git tag",
                 "optional": False}]

    @staticmethod
    def get_local_tag():
        from subprocess import check_output
        return check_output(
            ['git', 'describe', '--abbrev=0', '--tags']).strip()
