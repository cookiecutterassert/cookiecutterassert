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

from cookiecutterassert.rules.file_does_not_contain_snippet import FileDoesNotContainSnippetRule
from unittest.mock import patch
from pathlib import Path
import os.path
from cookiecutterassert import messager

currentFolder = os.path.dirname(os.path.abspath(__file__))
outputFolder = Path(currentFolder).parent.parent
testFolder = outputFolder
fileName = "example/fileWithSnippet.txt"
notExistingFileName = "notExistingFileName"
goodSnippetFile = "example/goodSnippet.txt"
badSnippetFile = "example/badSnippet.txt"

def test_execute_shouldLookForLineInFileAndReturnTrueIfItExists():
    fileDoesNotContainSnippet = FileDoesNotContainSnippetRule({}, testFolder, fileName, badSnippetFile)
    assert fileDoesNotContainSnippet.execute(outputFolder)

@patch("cookiecutterassert.messager.printError")
def test_execute_shouldLookForLineInFileAndReturnFalseIfItDoesNotExist(printMock):
    fileDoesNotContainSnippet = FileDoesNotContainSnippetRule({}, testFolder, fileName, goodSnippetFile)
    assert fileDoesNotContainSnippet.execute(outputFolder) == False
    printMock.assert_called_once_with("assertion fileDoesNotContainSnippet {0} {1} failed.  Matching lines from {1} not found in {2}/{0}.".format(fileName, goodSnippetFile, outputFolder))

@patch("cookiecutterassert.messager.printError")
def test_execute_shouldFailAndPrintIfFileDoesNotExist(printMock):
    fileDoesNotContainSnippet = FileDoesNotContainSnippetRule({}, testFolder, notExistingFileName, badSnippetFile)
    assert fileDoesNotContainSnippet.execute(outputFolder) == False
    printMock.assert_called_once_with("assertion fileDoesNotContainSnippet {0} {1} failed. {0} does not exist in {2}.".format(notExistingFileName, badSnippetFile, outputFolder)) 

@patch("cookiecutterassert.messager.printError")
def test_execute_shouldFailAndPrintIfSnippetDoesNotExist(printMock):
    fileDoesNotContainSnippet = FileDoesNotContainSnippetRule({}, testFolder, fileName, notExistingFileName)
    assert fileDoesNotContainSnippet.execute(outputFolder) == False
    printMock.assert_called_once_with("assertion fileDoesNotContainSnippet {0} {1} failed. {1} does not exist in {2}.".format(fileName, notExistingFileName, testFolder)) 
