# Copyright 2020 Ford Motor Company 

 

# Licensed under the Apache License, Version 2.0 (the "License"); 

# you may not use this file except in compliance with the License. 

# You may obtain a copy of the License at 

 

#     http://www.apache.org/licenses/LICENSE-2.0 

 

# Unless required by applicable law or agreed to in writing, software 

# distributed under the License is distributed on an "AS IS" BASIS, 

# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 

# See the License for the specific language governing permissions and 

# limitations under the License. 

import click
from cookiecutterassert import test_coordinator
import traceback
import sys
from cookiecutterassert.messager import printError, printMessage, printSuccess
from cookiecutterassert.options_parser import create_cli_options

def _run_tests(templatefolder, specific_test_folder, cli_options):
    if (specific_test_folder == None):
        return test_coordinator.runAllTestsInAllFolders(templatefolder, cli_options)
    else:
        return test_coordinator.runSpecificTestFolder(templatefolder, specific_test_folder, cli_options)

@click.command()
@click.option('--templatefolder', default='.', help='path of cookiecutter project directory, defaults to .')
@click.option('-vw',"--visible-whitespace", is_flag=True, default=False, help='make whitespace visble with symbols in place of common whitespace characters')
@click.argument('specific_test_folder', required=False)
def runAllTests(templatefolder, visible_whitespace, specific_test_folder):
    """Runs all test folders in the test directory or a single specific test folder if specified"""
    success = True
    cli_options = create_cli_options(visible_whitespace)
    try :
        success = _run_tests(templatefolder, specific_test_folder, cli_options)
    except:
        printError(traceback.format_exc())
        sys.exit(-1)

    if (not success):
        sys.exit(1)

if __name__ == '__main__':
    runAllTests()

