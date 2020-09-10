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

@click.command()
@click.option('--templatefolder', default='.', help='path of cookiecutter project directory, defaults to .')

def runAllTests(templatefolder):
    """Runs all test folders in the test directory"""
    success = True
    try :
        printMessage('Running all tests in %s' % templatefolder)
        success = test_coordinator.runAllTestsInAllFolders(templatefolder)
    except:
        printError(traceback.format_exc())
        sys.exit(-1)
    
    if (success):
        printSuccess('All tests passed')
    else :  # non-zero exit code to indicate failure
        printError('There were failing tests')
        sys.exit(1)

if __name__ == '__main__':
    runAllTests()

