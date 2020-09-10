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

from cookiecutterassert import test_folder_executor
from cookiecutterassert import cookie_cutter_interface
from cookiecutterassert import assertion_file_parser
import os.path
from unittest.mock import patch
import pytest
from cookiecutterassert import messager

templateFolder = "templateFolder"
testFolder = "testFolder"

class PassingRule:
    def __init__(self):
        self.executeCount = 0
        self.outputFolder = ""
    
    def execute(self, outputFolder):
        self.executeCount+=1
        self.outputFolder = outputFolder
        return True

class FailingRule:
    def __init__(self):
        self.executeCount = 0
        self.outputFolder = ""
    
    def execute(self, outputFolder):
        self.executeCount+=1
        self.outputFolder = outputFolder
        return False

def isConfigYmlOrAssertionsYml(fileName):
    return fileName.endswith("/config.yml") or fileName.endswith("/assertions.yml") or fileName.endswith("/defaultConfig.yml")

def isConfigYamlOrAssertionsYaml(fileName):
    return fileName.endswith("/config.yaml") or fileName.endswith("/assertions.yaml") or fileName.endswith("/defaultConfig.yaml")

@pytest.fixture
def fakeRuleList():
    return [
        PassingRule(),
        PassingRule()
    ]

@patch("cookiecutterassert.test_folder_executor.print")
@patch('cookiecutterassert.assertion_file_parser.parseAssertionFile')
@patch('os.path.isfile')
@patch('cookiecutterassert.cookie_cutter_interface.generateFilesFromTemplate')
def test_executeAllTestsInFolder_shouldGenerateTemplatesToTestBuildFolder(mockGenerateFilesFromTemplate, mockIsfile, mockAssertionFileParser, printMock, fakeRuleList):
    expectedConfigFile = testFolder+"/config.yaml"
    expectedDefaultConfigFile = templateFolder+"/defaultConfig.yaml"
    expectedOutputFolder = testFolder+"/build"
    mockIsfile.side_effect = isConfigYamlOrAssertionsYaml
    mockAssertionFileParser.return_value = fakeRuleList

    test_folder_executor.executeAllTestsInFolder(templateFolder, testFolder)

    mockGenerateFilesFromTemplate.assert_called_once_with(templateFolder, expectedConfigFile, expectedOutputFolder, expectedDefaultConfigFile)


@patch("cookiecutterassert.test_folder_executor.print")
@patch('cookiecutterassert.assertion_file_parser.parseAssertionFile')
@patch('os.path.isfile')
@patch('cookiecutterassert.cookie_cutter_interface.generateFilesFromTemplate')
def test_executeAllTestsInFolder_shouldGenerateTemplatesToTestBuildFolderIfConfigDotYml(mockGenerateFilesFromTemplate, mockIsfile, mockAssertionFileParser, printMock, fakeRuleList):
    expectedConfigFile = testFolder+"/config.yml"
    expectedDefaultConfigFile = templateFolder+"/defaultConfig.yml"
    expectedOutputFolder = testFolder+"/build"
    mockIsfile.side_effect = isConfigYmlOrAssertionsYml
    mockAssertionFileParser.return_value = fakeRuleList

    test_folder_executor.executeAllTestsInFolder(templateFolder, testFolder)

    mockGenerateFilesFromTemplate.assert_called_once_with(templateFolder, expectedConfigFile, expectedOutputFolder, expectedDefaultConfigFile)


@patch("cookiecutterassert.test_folder_executor.print")
@patch('cookiecutterassert.assertion_file_parser.parseAssertionFile')
@patch('os.path.isfile')
@patch('cookiecutterassert.cookie_cutter_interface.generateFilesFromTemplate')
def test_executeAllTestsInFolder_shouldParseAndExecuteRules(mockGenerateFilesFromTemplate, mockIsfile, mockAssertionFileParser, printMock, fakeRuleList):
    templateFolder = "templateFolder"
    testFolder = "testFolder"
    expectedOutputFolder = testFolder+"/build"
    expectedAssertionFile = testFolder+"/assertions.yaml"
    mockIsfile.side_effect = isConfigYamlOrAssertionsYaml
    mockAssertionFileParser.return_value = fakeRuleList

    actualResult = test_folder_executor.executeAllTestsInFolder(templateFolder, testFolder)

    mockAssertionFileParser.assert_called_once_with(expectedAssertionFile, testFolder)
    assert actualResult == True
    assert fakeRuleList[0].executeCount == 1
    assert fakeRuleList[0].outputFolder == expectedOutputFolder
    assert fakeRuleList[1].executeCount == 1
    assert fakeRuleList[1].outputFolder == expectedOutputFolder

@patch("cookiecutterassert.test_folder_executor.print")
@patch('cookiecutterassert.assertion_file_parser.parseAssertionFile')
@patch('os.path.isfile')
@patch('cookiecutterassert.cookie_cutter_interface.generateFilesFromTemplate')
def test_executeAllTestsInFolder_shouldParseAndExecuteRulesFromAssertionsDotYml(mockGenerateFilesFromTemplate, mockIsfile, mockAssertionFileParser, printMock, fakeRuleList):
    templateFolder = "templateFolder"
    testFolder = "testFolder"
    expectedOutputFolder = testFolder+"/build"
    expectedAssertionFile = testFolder+"/assertions.yml"
    mockIsfile.side_effect = isConfigYmlOrAssertionsYml
    mockAssertionFileParser.return_value = fakeRuleList

    actualResult = test_folder_executor.executeAllTestsInFolder(templateFolder, testFolder)

    mockAssertionFileParser.assert_called_once_with(expectedAssertionFile, testFolder)

@patch("cookiecutterassert.test_folder_executor.print")
@patch('cookiecutterassert.assertion_file_parser.parseAssertionFile')
@patch('os.path.isfile')
@patch('cookiecutterassert.cookie_cutter_interface.generateFilesFromTemplate')
def test_executeAllTestsInFolder_shouldFailIfARuleFails(mockGenerateFilesFromTemplate, mockIsfile, mockAssertionFileParser, printMock, fakeRuleList):
    templateFolder = "templateFolder"
    testFolder = "testFolder"
    expectedOutputFolder = testFolder+"/build"
    expectedAssertionFile = testFolder+"/assertions.yml"
    mockIsfile.side_effect = isConfigYmlOrAssertionsYml
    fakeRuleList[1] = FailingRule()
    mockAssertionFileParser.return_value = fakeRuleList

    actualResult = test_folder_executor.executeAllTestsInFolder(templateFolder, testFolder)

    assert actualResult == False
    assert fakeRuleList[0].executeCount == 1
    assert fakeRuleList[1].executeCount == 1

@patch("cookiecutterassert.test_folder_executor.print")
@patch('cookiecutterassert.assertion_file_parser.parseAssertionFile')
@patch('os.path.isfile')
@patch('cookiecutterassert.cookie_cutter_interface.generateFilesFromTemplate')
def test_executeAllTestsInFolder_shouldBreakOnFirstFailure(mockGenerateFilesFromTemplate, mockIsfile, mockAssertionFileParser, printMock, fakeRuleList):
    templateFolder = "templateFolder"
    testFolder = "testFolder"
    expectedOutputFolder = testFolder+"/build"
    expectedAssertionFile = testFolder+"/assertions.yml"
    mockIsfile.side_effect = isConfigYmlOrAssertionsYml
    fakeRuleList[0] = FailingRule()
    mockAssertionFileParser.return_value = fakeRuleList

    actualResult = test_folder_executor.executeAllTestsInFolder(templateFolder, testFolder)

    assert actualResult == False
    assert fakeRuleList[0].executeCount == 1
    assert fakeRuleList[1].executeCount == 0

@patch("cookiecutterassert.messager.printMessage")
@patch('cookiecutterassert.assertion_file_parser.parseAssertionFile')
@patch('os.path.isfile')
@patch('cookiecutterassert.cookie_cutter_interface.generateFilesFromTemplate')
def test_executeAllTestsInFolder_shouldPrintTestFolderBeingRun(mockGenerateFilesFromTemplate, mockIsfile, mockAssertionFileParser, printMock, fakeRuleList):
    templateFolder = "templateFolder"
    testFolder = "testFolder"
    expectedOutputFolder = testFolder+"/build"
    expectedAssertionFile = testFolder+"/assertions.yaml"
    mockIsfile.side_effect = isConfigYamlOrAssertionsYaml
    mockAssertionFileParser.return_value = fakeRuleList

    actualResult = test_folder_executor.executeAllTestsInFolder(templateFolder, testFolder)
    
    printMock.assert_called_once_with("---Starting tests for "+testFolder)

@patch("cookiecutterassert.messager.printError")
@patch('cookiecutterassert.assertion_file_parser.parseAssertionFile')
@patch('os.path.isfile')
@patch('cookiecutterassert.cookie_cutter_interface.generateFilesFromTemplate')
def test_executeAllTestsInFolder_shouldFailIfNoAssertiondsFound(mockGenerateFilesFromTemplate, mockIsfile, mockAssertionFileParser, printMock, fakeRuleList):
    templateFolder = "templateFolder"
    testFolder = "testFolder"
    expectedOutputFolder = testFolder+"/build"
    expectedAssertionFile = testFolder+"/assertions.yaml"
    mockIsfile.side_effect = isConfigYamlOrAssertionsYaml

    mockAssertionFileParser.return_value = []

    actualResult = test_folder_executor.executeAllTestsInFolder(templateFolder, testFolder)

    assert actualResult == False
    assert fakeRuleList[0].executeCount == 0
    assert fakeRuleList[1].executeCount == 0
    printMock.assert_called_with("ERROR: No assertions found in test folder: {}".format(testFolder))