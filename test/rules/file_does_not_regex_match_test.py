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

from cookiecutterassert.rules.file_does_not_regex_match import FileDoesNotRegexMatchRule
from unittest.mock import patch
from pathlib import Path
import os.path
from cookiecutterassert import messager

currentFolder = os.path.dirname(os.path.abspath(__file__))
outputFolder = Path(currentFolder).parent.parent
testFolder = "someoutput"

regex = "^lo+king\\sfor.*$"


def test_execute_shouldLookForMatchingLineInFileAndReturnTrueIfItDoesNotExists():
    fileName = "example/fileWithoutLine.txt"
    fileContainsLineRule = FileDoesNotRegexMatchRule({}, testFolder, fileName, regex)
    assert fileContainsLineRule.execute(outputFolder)

@patch("cookiecutterassert.messager.printError")
def test_execute_shouldLookForMatchingLineInFileAndReturnFalseIfItDoesExist(printMock):
    fileName = "example/fileWithLine.txt"
    fileContainsLineRule = FileDoesNotRegexMatchRule({}, testFolder, fileName, regex)
    assert fileContainsLineRule.execute(outputFolder) == False
    printMock.assert_called_once_with("assertion fileDoesNotHaveMatchingLine {0} {1} failed.  Matching line found in {2}/{0}.".format(fileName, regex, outputFolder)) 

@patch("cookiecutterassert.messager.printError")
def test_execute_shouldFailAndPrintIfFileDoesNotExist(printMock):
    fileName = "example/aFileThatDoesNotExist"
    fileContainsLineRule = FileDoesNotRegexMatchRule({}, testFolder, fileName, regex)
    assert fileContainsLineRule.execute(outputFolder) == False
    printMock.assert_called_once_with("assertion fileDoesNotHaveMatchingLine {0} {1} failed. {0} does not exist in {2}.".format(fileName, regex, outputFolder)) 

@patch("cookiecutterassert.messager.printError")
def test_execute_shouldFailAndPrintIfFileDoesNotExist_case_sensitive(printMock):
    fileName = "example/fileWithoutline.txt"
    fileContainsLineRule = FileDoesNotRegexMatchRule({}, testFolder, fileName, regex)
    assert fileContainsLineRule.execute(outputFolder) == False
    printMock.assert_called_once_with("assertion fileDoesNotHaveMatchingLine {0} {1} failed. {0} does not exist in {2}.".format(fileName, regex, outputFolder)) 
