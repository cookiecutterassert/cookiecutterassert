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

from cookiecutterassert import folder_scanner
from cookiecutterassert import test_folder_executor
from cookiecutterassert import messager
import os
from cookiecutterassert import stale_test_folder_cleanup

def runAllTestsInAllFolders(project_root_folder, cli_options):
    messager.printMessage(f'Running all tests in {project_root_folder}')
    root_test_folder = _getRootTestFolder(project_root_folder)
    if (root_test_folder == None):
        return False

    testFolders = folder_scanner.findAllTestFolders(root_test_folder)
    
    if (len(testFolders) == 0):
        messager.printError(f'No test cases found. Expecting to find one or more subdirectories in {root_test_folder} with valid config.yaml and assertions.yaml files')
        return False

    failureCount = 0
    successCount = 0
    for folder in testFolders :
        folderSuccess = test_folder_executor.executeAllTestsInFolder(project_root_folder, folder, cli_options)
        if (folderSuccess):
            successCount += 1
        else:
            failureCount += 1

    stale_test_folder_cleanup.delete_stale_test_folders(root_test_folder)

    _printResults(failureCount, successCount)

    return failureCount == 0

def runSpecificTestFolder(project_root_folder, test_folder_name, cli_options):
    messager.printMessage(f'running test {test_folder_name} in {project_root_folder}')
    root_test_folder = _getRootTestFolder(project_root_folder)
    if (root_test_folder == None):
        return False
    
    test_folder_path = root_test_folder+'/'+test_folder_name
    if (not os.path.isdir(test_folder_path)):
        messager.printError(f'No test folder found, expecting to find one at {test_folder_path}')
        return False
    allTestsPass = test_folder_executor.executeAllTestsInFolder(project_root_folder, test_folder_path, cli_options)
    if (allTestsPass):
        _printResults(0, 1)
    else:
        _printResults(1, 0)

    return allTestsPass

def _getRootTestFolder(project_root_folder):
    root_test_folder = project_root_folder+'/test'
    if (not os.path.isdir(root_test_folder)):
        messager.printError(f'No test folder found, expecting to find one at {root_test_folder}')
        return None
    else:
        return root_test_folder 

def _printResults(failureCount, successCount):
    if (failureCount == 0):
        messager.printSuccess(f'{successCount} tests passed')
    else:
        messager.printError(f'There were {failureCount} failing and {successCount} passing tests')