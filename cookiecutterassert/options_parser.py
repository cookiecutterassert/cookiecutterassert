
from cookiecutterassert.rules.option_names import VISIBLE_WHITESPACE

def create_cli_options(visible_whitepace):
    options = {}
    if visible_whitepace:
        options[VISIBLE_WHITESPACE] = True
    return options