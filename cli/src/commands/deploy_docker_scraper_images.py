from .abstract_command import AbstractCommand


class DeployDockerScraperImages(AbstractCommand):
    def get_name(self):
        return "deploy:scraper"

    def get_description(self):
        return "Deploy docker scraper images"

    def run(self, args):
        return self.exec_shell_command(
            ["./cli/scripts/publish_docker_scraper_images.sh"])
