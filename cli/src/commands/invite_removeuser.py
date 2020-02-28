from .abstract_command import AbstractCommand


class InviteRemoveUser(AbstractCommand):
    def get_name(self):
        return "invite:remove_user"

    def get_description(self):
        return "Uninvite to an DocSearch index an email"

    def get_usage(self):
        return super(InviteRemoveUser, self).get_usage() + " config email"

    def get_options(self):
        return [
            {"name": "config", "description": "name of the config"},
            {"name": "email", "description": "email to add"}
        ]

    def run(self, args):
        from deployer.src.algolia_internal_api import remove_user_from_index

        remove_user_from_index(args[0], args[1])
