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

from cookiecutterassert.rules.file_matches import FileMatchesRule
from unittest.mock import patch, MagicMock
from cookiecutterassert.rules import rules_util
import filecmp
import os.path

fileName = "some/test/file"
fixturePath = "fixture"
outputFolder = "someoutput/build"
testFolder = "someoutput"

wrongOutputLines = [
    "someline"
]

fixtureFileLines = [
    "correctline"
]


def readLinesSideEffect(fileToRead):
    if (fileToRead == fixturePath):
        return fixtureFileLines
    elif (fileToRead == fileName):
        return wrongOutputLines
    else:
        return None


def styleSideEffect(message, fg):
    return "ANSI STYLED "+fg + ":: "+message


def throwFixtureFileNotFound():
    raise FileNotFoundError(os.path.join(testFolder, fixturePath))


def throwGeneratedFileNotFound():
    raise FileNotFoundError(os.path.join(outputFolder, fileName))


def fixtureFileDoesNotExist(path):
    return path != os.path.join(testFolder, fixturePath)


def fileNameDoesNotExist(path):
    return path != os.path.join(outputFolder, fileName)


@patch("os.path.exists")
@patch("filecmp.cmp")
def test_execute_shouldReturnTrueIfTheFilesMatch(filecmpMock, pathExistsMock):
    pathExistsMock.return_value = True
    filecmpMock.return_value = True

    fileMatchesRule = FileMatchesRule(testFolder, fileName, fixturePath)
    assert fileMatchesRule.execute(outputFolder)
    filecmpMock.assert_called_once_with(os.path.join(
        outputFolder, fileName), os.path.join(testFolder, fixturePath), shallow=False)


@patch("os.path.exists")
@patch("filecmp.cmp")
@patch("cookiecutterassert.messager.printError")
def test_execute_shouldReturnFalseIfTheFilesDoNotMatch(printMock, filecmpMock, pathExistsMock):
    filecmpMock.return_value = False
    pathExistsMock.return_value = True

    fileMatchesRule = FileMatchesRule(testFolder, fileName, fixturePath)
    fileMatchesRule.printDifferences = MagicMock(name='printDifferences')
    assert not fileMatchesRule.execute(outputFolder)
    printMock.assert_called_once_with(
        "assertion fileMatches " + fileName+" "+fixturePath + " failed.  Files differ")


@patch("os.path.exists")
@patch("filecmp.cmp")
@patch("cookiecutterassert.messager.printError")
def test_execute_shouldReturnFalseAndNotThrowIfFixtureDoesNotExist(printMock, filecmpMock, pathExistsMock):
    filecmpMock.side_effect = throwFixtureFileNotFound
    pathExistsMock.side_effect = fixtureFileDoesNotExist
    fileMatchesRule = FileMatchesRule(testFolder, fileName, fixturePath)

    assert not fileMatchesRule.execute(outputFolder)
    printMock.assert_called_once_with("assertion fileMatches " + fileName+" "+fixturePath +
                                      " failed.  "+os.path.abspath(os.path.join(testFolder, fixturePath))+" does not exist")


@patch("os.path.exists")
@patch("filecmp.cmp")
@patch("cookiecutterassert.messager.printError")
def test_execute_shouldReturnFalseAndNotThrowIfFileDoesNotExist(printMock, filecmpMock, pathExistsMock):
    filecmpMock.side_effect = throwGeneratedFileNotFound
    pathExistsMock.side_effect = fileNameDoesNotExist
    fileMatchesRule = FileMatchesRule(testFolder, fileName, fixturePath)

    assert not fileMatchesRule.execute(outputFolder)
    printMock.assert_called_once_with("assertion fileMatches " + fileName+" "+fixturePath +
                                      " failed.  "+os.path.abspath(os.path.join(outputFolder, fileName))+" does not exist")


@patch("cookiecutterassert.rules.rules_util.readLinesFromFile")
@patch("difflib.unified_diff")
@patch("click.style")
@patch("click.echo")
def test_printDifferencesPrintsFileDiff(echoMock, styleMock, diffMock, readLinesMock):
    readLinesMock.side_effect = readLinesSideEffect
    diffLines = [
        "+ test output line",
        "- test fixture line"
    ]
    diffMock.return_value = diffLines
    styleMock.side_effect = styleSideEffect

    fileMatchesRule = FileMatchesRule(testFolder, fileName, fixturePath)
    fileMatchesRule.printDifferences(fileName, fixturePath)

    diffMock.assert_called_once_with(wrongOutputLines, fixtureFileLines, fromfile=fileName, tofile=fixturePath)
    echoMock.assert_any_call("ANSI STYLED blue:: "+diffLines[0])
    echoMock.assert_any_call("ANSI STYLED yellow:: "+diffLines[1])

@patch("cookiecutterassert.rules.rules_util.readLinesFromFile")
@patch("difflib.unified_diff")
@patch("click.style")
@patch("click.echo")
def test_printDifferencesPrintsFileDiff(echoMock, styleMock, diffMock, readLinesMock):
    readLinesMock.side_effect = readLinesSideEffect
    diffLines = [
        "+ test output line",
        "- test fixture line"
    ]
    diffMock.return_value = diffLines
    styleMock.side_effect = styleSideEffect

    fileMatchesRule = FileMatchesRule(testFolder, fileName, fixturePath)
    fileMatchesRule.printDifferences(fileName, fixturePath)

    diffMock.assert_called_once_with(wrongOutputLines, fixtureFileLines, fromfile=fileName, tofile=fixturePath)
    echoMock.assert_any_call("ANSI STYLED blue:: "+diffLines[0])
    echoMock.assert_any_call("ANSI STYLED yellow:: "+diffLines[1])

@patch("cookiecutterassert.messager.printError")
@patch("cookiecutterassert.rules.rules_util.readLinesFromFile")
def test_printDifferencesHandlesBinary(readLinesMock, printMock):
    readLinesMock.side_effect = UnicodeDecodeError('encoding', bytearray(1) , 0, 1, 'test error')
    
    fileMatchesRule = FileMatchesRule(testFolder, fileName, fixturePath)
    fileMatchesRule.printDifferences(fileName, fixturePath)

    printMock.assert_called_once_with("One or both files are binary, unable to print differences")