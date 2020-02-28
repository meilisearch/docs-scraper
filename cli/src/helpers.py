def get_color(color=4):
    if color == 1:
        return "\033[0;32m"
    elif color == 2:
        return "\033[33m"
    elif color == 3:
        return "\033[1;33m\033[1;41m"
    else:
        return "\033[0m"


def printer(text, color=4, no_ansi=False):
    if no_ansi is True:
        print(text)
    else:
        print(get_color(color) + text + get_color())


def print_error(message):
    line = " " * (len(message) + 4)
    printer(line, 3)
    printer(" " * 2 + message + " " * 2, 3)
    printer(line, 3)


def print_command_help(command, no_ansi=False):
    printer("Usage:", 2)
    printer(command.get_usage())
    printer("")
    printer("Options:", 2)

    options = command.get_options()
    options = sorted(options, key=lambda x: x["name"])
    options = options + [
        {"name": "--help", "description": "Display help message"}]

    longest_option = 0
    for option in options:
        longest_option = max(longest_option, len(option["name"]))

    for option in options:
        nb_spaces = longest_option + 2 - len(option["name"])
        printer("  " + get_color(1) + option["name"] + get_color() + (
            " " * nb_spaces) + option["description"])

    printer("")
    printer("Help:", 2)
    printer("  " + command.get_description())
