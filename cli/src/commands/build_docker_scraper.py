from .abstract_build_docker import AbstractBuildDocker


class BuildDockerScraper(AbstractBuildDocker):
    def get_name(self):
        return "docker:build"

    def get_description(self):
        return "Build scraper images (dev, prod)"

    def get_options(self):
        options = super(BuildDockerScraper, self).get_options()

        options.append({"name": "test",
                        "description": "build the test image",
                        "optional": False})
        return options

    def run(self, args):

        # Order of options matter
        local_tag = self.get_option("local_tag", args)
        test = self.get_option("test", args)

        if test:
            return self.build_docker_file("scraper/dev/docker/Dockerfile.test",
                                          "algolia/docsearch-scraper-test",
                                          local_tag=local_tag)

        code = self.build_docker_file("scraper/dev/docker/Dockerfile.base",
                                      "algolia/docsearch-scraper-base",
                                      local_tag=local_tag)

        if code != 0:
            return code
        code = self.build_docker_file("scraper/dev/docker/Dockerfile.dev",
                                      local_tag=local_tag)
        if code != 0:
            return code
        return self.build_docker_file("scraper/dev/docker/Dockerfile",
                                      "algolia/docsearch-scraper", local_tag=local_tag)
