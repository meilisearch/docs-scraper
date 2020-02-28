from .abstract_command import AbstractCommand


class GenerateEmail(AbstractCommand):
    def get_name(self):
        return "generate:email"

    def get_description(self):
        return "Generate the email for a docsearch"

    def get_options(self):
        return [{"name": "name",
                 "description": "name of the docsearch you want to generate the email"}]

    def run(self, args):
        import pyperclip
        from deployer.src.snippeter import get_email_for_config

        email_content = get_email_for_config(args[0])
        pyperclip.copy(email_content)

        print(email_content)
        print("Config copied to clipboard [OK]")
        print("")
