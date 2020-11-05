from cookiecutterassert import options_parser
from cookiecutterassert.rules.option_names import VISIBLE_WHITESPACE

def test_create_cli_options_shouldCreateOptionsObjectFromDefautCLIOptions():
    assert {} == options_parser.create_cli_options(False)

def test_create_cli_options_shouldCreateOptionsWithVisibleWhitespace():
    assert {VISIBLE_WHITESPACE: True} == options_parser.create_cli_options(True)
    