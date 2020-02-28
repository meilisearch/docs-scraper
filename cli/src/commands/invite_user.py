from .abstract_command import AbstractCommand


class InviteUser(AbstractCommand):
    def get_name(self):
        return "invite:user"

    def get_description(self):
        return "Invite to an DocSearch index an email"

    def get_usage(self):
        return super(InviteUser, self).get_usage() + " config email"

    def get_options(self):
        return [
            {"name": "config", "description": "name of the config"},
            {"name": "email", "description": "email to add"}
        ]

    def run(self, args):
        from deployer.src.algolia_internal_api import add_user_to_index

        add_user_to_index(args[0], args[1])
