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


folderAName = 'folderA'
folderBName = 'folderB'

rootFolder='./testFolder'
rootTestFolder = rootFolder+'/test'
testFolderA = rootTestFolder+'/'+folderAName
testFolderB = rootTestFolder+'/'+folderBName


cli_options = {"someoption": True}

@pytest.fixture
def testFolderSet():
    folderSet = []
    folderSet.append(testFolderA)
    folderSet.append(testFolderB)
    return folderSet

def failTestA(templateFolder, testFolder, cli_options):
    return testFolder != testFolderA

def rootTestFolderDoesNotExist(folder_path):
    return folder_path != rootTestFolder

def folderADoesNotExist(folder_path):
    return folder_path != testFolderA

@patch('cookiecutterassert.messager.printError')
@patch('cookiecutterassert.messager.printSuccess')
@patch('cookiecutterassert.messager.printMessage')
@patch('os.path.isdir')
@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
@patch('cookiecutterassert.folder_scanner.findAllTestFolders')
@patch('cookiecutterassert.stale_test_folder_cleanup.delete_stale_test_folders')
def test_runAllTestsInAllFolders_shouldScanAllFoldersAndExecuteTests(mock_delete_stale_test_folders, mockFindAllTestFolders, mockExecuteAllTestsInFolder, mockIsDir, mockPrintMessage, mockPrintSuccess, mockPrintError, testFolderSet):
    mockFindAllTestFolders.return_value = testFolderSet
    mockExecuteAllTestsInFolder.return_value = True
    mockIsDir.return_value = True

    actualResult = test_coordinator.runAllTestsInAllFolders(rootFolder, cli_options)
    
    mockFindAllTestFolders.assert_called_with(rootTestFolder)
    mockExecuteAllTestsInFolder.assert_any_call(rootFolder, testFolderA, cli_options)
    mockExecuteAllTestsInFolder.assert_any_call(rootFolder, testFolderB, cli_options)
    mock_delete_stale_test_folders.assert_called_once_with(rootTestFolder)
    mockPrintMessage.assert_called_with(f'Running all tests in {rootFolder}')
    mockPrintSuccess.assert_called_with('2 tests passed')
    mockPrintError.assert_not_called()
    assert actualResult == True


@patch('cookiecutterassert.messager.printError')
@patch('cookiecutterassert.messager.printSuccess')
@patch('os.path.isdir')
@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
@patch('cookiecutterassert.folder_scanner.findAllTestFolders')
@patch('cookiecutterassert.stale_test_folder_cleanup.delete_stale_test_folders')
def test_runAllTestsInAllFolders_shouldReturnFalseIfAnyFolderFails(mock_delete_stale_test_folders, mockFindAllTestFolders, mockExecuteAllTestsInFolder, mockIsDir,  mockPrintSuccess, mockPrintError, testFolderSet):
    mockFindAllTestFolders.return_value = testFolderSet
    mockExecuteAllTestsInFolder.side_effect = failTestA
    mockIsDir.return_value = True

    actualResult = test_coordinator.runAllTestsInAllFolders(rootFolder, cli_options)

    assert actualResult == False
    mockPrintSuccess.assert_not_called()
    mockPrintError.assert_called_with('There were 1 failing and 1 passing tests')


@patch('cookiecutterassert.messager.printError')
@patch('os.path.isdir')
@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
@patch('cookiecutterassert.folder_scanner.findAllTestFolders')
@patch('cookiecutterassert.stale_test_folder_cleanup.delete_stale_test_folders')
def test_runAllTestsInAllFolders_should_return_false_if_test_folder_does_not_exist(mock_delete_stale_test_folders, mockFindAllTestFolders, mockExecuteAllTestsInFolder, mockIsDir, mockPrintError, testFolderSet):
    mockFindAllTestFolders.return_value = testFolderSet
    mockExecuteAllTestsInFolder.return_value = True
    mockIsDir.return_value = False
    actualResult = test_coordinator.runAllTestsInAllFolders(rootFolder, {})

    assert actualResult == False
    mockIsDir.assert_called_with(rootTestFolder)
    mockPrintError.assert_called_with(f'No test folder found, expecting to find one at {rootTestFolder}')

@patch('cookiecutterassert.messager.printError')
@patch('os.path.isdir')
@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
@patch('cookiecutterassert.folder_scanner.findAllTestFolders')
@patch('cookiecutterassert.stale_test_folder_cleanup.delete_stale_test_folders')
def test_runAllTestsInAllFolders_should_return_false_if_no_test_cases(mock_delete_stale_test_folders, mockFindAllTestFolders, mockExecuteAllTestsInFolder, mockIsDir, mockPrintError, testFolderSet):
    mockFindAllTestFolders.return_value = set()
    mockExecuteAllTestsInFolder.return_value = True
    mockIsDir.return_value = True
    actualResult = test_coordinator.runAllTestsInAllFolders(rootFolder, {})

    assert actualResult == False
    mockPrintError.assert_called_with(f'No test cases found. Expecting to find one or more subdirectories in {rootTestFolder} with valid config.yaml and assertions.yaml files')


@patch('cookiecutterassert.messager.printError')
@patch('cookiecutterassert.messager.printSuccess')
@patch('cookiecutterassert.messager.printMessage')
@patch('os.path.isdir')
@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
def test_runSpecificTestFolder_shouldExecuteTests(mockExecuteAllTestsInFolder, mockIsDir, mockPrintMessage, mockPrintSuccess, mockPrintError, testFolderSet):

    mockExecuteAllTestsInFolder.return_value = True
    mockIsDir.return_value = True

    actualResult = test_coordinator.runSpecificTestFolder(rootFolder, folderAName, cli_options)
    
    mockExecuteAllTestsInFolder.assert_called_with(rootFolder, testFolderA, cli_options)
    assert actualResult == True
    mockPrintMessage.assert_called_with(f'running test {folderAName} in {rootFolder}')
    mockPrintSuccess.assert_called_with('1 tests passed')
    mockPrintError.assert_not_called()

@patch('cookiecutterassert.messager.printError')
@patch('cookiecutterassert.messager.printSuccess')
@patch('os.path.isdir')
@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
def test_runSpecificTestFolder_shouldReturnFalseIfFolderFails(mockExecuteAllTestsInFolder, mockIsDir, mockPrintSuccess, mockPrintError, testFolderSet):
    mockExecuteAllTestsInFolder.return_value = False
    mockIsDir.return_value = True

    actualResult = test_coordinator.runSpecificTestFolder(rootFolder, folderAName, cli_options)
    
    mockExecuteAllTestsInFolder.assert_called_with(rootFolder, testFolderA, cli_options)
    assert actualResult == False
    mockPrintSuccess.assert_not_called()
    mockPrintError.assert_called_with('There were 1 failing and 0 passing tests')


@patch('cookiecutterassert.messager.printError')
@patch('os.path.isdir')
@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
def test_runSpecificTestFolder_shouldReturnFalseIfTestFolderDoesNotExit(mockExecuteAllTestsInFolder, mockIsDir, mockPrintError, testFolderSet):
    mockExecuteAllTestsInFolder.return_value = False
    mockIsDir.side_effect = rootTestFolderDoesNotExist

    actualResult = test_coordinator.runSpecificTestFolder(rootFolder, folderAName, cli_options)
    
    mockExecuteAllTestsInFolder.assert_not_called()
    assert actualResult == False
    mockPrintError.assert_called_with(f'No test folder found, expecting to find one at {rootTestFolder}')

@patch('cookiecutterassert.messager.printError')
@patch('os.path.isdir')
@patch('cookiecutterassert.test_folder_executor.executeAllTestsInFolder')
def test_runSpecificTestFolder_shouldReturnFalseIfTestCaseFolderDoesNotExit(mockExecuteAllTestsInFolder, mockIsDir, mockPrintError, testFolderSet):
    mockExecuteAllTestsInFolder.return_value = False
    mockIsDir.side_effect = folderADoesNotExist

    actualResult = test_coordinator.runSpecificTestFolder(rootFolder, folderAName, cli_options)
    
    mockExecuteAllTestsInFolder.assert_not_called()
    assert actualResult == False
    mockPrintError.assert_called_with(f'No test folder found, expecting to find one at {testFolderA}')