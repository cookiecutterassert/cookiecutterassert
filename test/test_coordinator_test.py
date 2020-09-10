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

from cookiecutterassert import test_coordinator
from cookiecutterassert import test_folder_executor
from cookiecutterassert import folder_scanner
from unittest.mock import patch
import pytest

rootFolder='./testFolder'
rootTestFolder = rootFolder+'/test'
testFolderA = rootTestFolder+'/folderA'
testFolderB = rootTestFolder+'/folderB'

@pytest.fixture
def testFolderSet():
    folderSet = set()
    folderSet.add(testFolderA)
    folderSet.add(testFolderB)
    return folderSet

def failTestA(templateFolder, testFolder):
    return testFolder != testFolderA

@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
@patch('cookiecutterassert.folder_scanner.findAllTestFolders')
def test_runAllTestsInAllFolders_shouldScanAllFoldersAndExecuteTests(mockFindAllTestFolders, mockExecuteAllTestsInFolder, testFolderSet):
    mockFindAllTestFolders.return_value = testFolderSet
    mockExecuteAllTestsInFolder.return_value = True

    actualResult = test_coordinator.runAllTestsInAllFolders(rootFolder)
    
    mockFindAllTestFolders.assert_called_with(rootTestFolder)
    mockExecuteAllTestsInFolder.assert_any_call(rootFolder, testFolderA)
    mockExecuteAllTestsInFolder.assert_any_call(rootFolder, testFolderB)
    assert actualResult == True

@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
@patch('cookiecutterassert.folder_scanner.findAllTestFolders')
def test_runAllTestsInAllFolders_shouldReturnFalseIfAnyFolderFails(mockFindAllTestFolders, mockExecuteAllTestsInFolder, testFolderSet):
    mockFindAllTestFolders.return_value = testFolderSet
    mockExecuteAllTestsInFolder.side_effect = failTestA

    actualResult = test_coordinator.runAllTestsInAllFolders(rootFolder)

    assert actualResult == False

