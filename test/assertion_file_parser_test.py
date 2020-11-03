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

from cookiecutterassert import assertion_file_parser
from pathlib import Path
from cookiecutterassert.rules.path_exists import PathExistsRule
from cookiecutterassert.rules.path_not_exists import PathNotExistsRule
from cookiecutterassert.rules.file_matches import FileMatchesRule
from cookiecutterassert.rules.run_script import RunScriptRule
from cookiecutterassert.rules.file_contains_line import FileContainsLineRule
from cookiecutterassert.rules.file_does_not_contain_line import FileDoesNotContainLineRule
from cookiecutterassert.rules.file_has_regex_match_line import FileHasRegexMatchLineRule
from cookiecutterassert.rules.file_does_not_regex_match import FileDoesNotRegexMatchRule
from cookiecutterassert.rules.file_contains_snippet_rule import FileContainsSnippetRule
from cookiecutterassert.rules.file_does_not_contain_snippet import FileDoesNotContainSnippetRule
from cookiecutterassert import messager
from unittest.mock import patch
from cookiecutterassert.rules.option_names import VISIBLE_WHITESPACE

import os.path


def test_parseAssertionFile_shouldReturnAssertionRuleArray():
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    testFolder = Path(currentFolder).parent.joinpath("example")
    assertionFile = testFolder.joinpath("sampleAssertionFile.yaml")

    expectedRules = []
    expectedRules.append(PathExistsRule({}, str(testFolder), "foo.txt"))
    expectedRules.append(PathExistsRule({}, str(testFolder), "bin"))
    expectedRules.append(PathNotExistsRule({}, str(testFolder), "missingFile"))
    expectedRules.append(FileMatchesRule({}, str(testFolder), "build.gradle", "expectedBuild.gradle"))
    expectedRules.append(RunScriptRule({}, str(testFolder), "MyApp", "./gradlew clean build"))
    expectedRules.append(FileContainsLineRule({}, str(testFolder), "MyApp/foo", "this line should exist"))
    expectedRules.append(FileDoesNotContainLineRule({}, str(testFolder), "MyApp/foo", "this line should not exist"))
    expectedRules.append(FileHasRegexMatchLineRule({}, str(testFolder), "MyApp/foo", "^lo+king \\sfor.*$"))
    expectedRules.append(FileDoesNotRegexMatchRule({}, str(testFolder), "MyApp/foo", "^lo+king\\s[fdfgd]{4} or.*$"))
    expectedRules.append(FileContainsSnippetRule({}, str(testFolder), "MyApp/foo", "goodSnippet.txt"))
    expectedRules.append(FileDoesNotContainSnippetRule({}, str(testFolder), "MyApp/foo", "badSnippet.txt"))

    actualRules = assertion_file_parser.parseAssertionFile(str(assertionFile), str(testFolder))

    assert expectedRules == actualRules

@patch('cookiecutterassert.messager.printError')
def test_parseAssertionFile_shouldReturnNullAndPrintMessageIfBadRule(printErrorMock):
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    testFolder = Path(currentFolder).parent.joinpath("example")
    assertionFile = testFolder.joinpath("sampleAssertionFileWithUnparseableAssertion.yaml")

    expectedRules = []
    expectedErrorMessage = "Unable to parse assertion file {}.  Error on assertion \"sdjhfs sdhjfgs 6463\"".format(str(assertionFile))
    
    actualRules = assertion_file_parser.parseAssertionFile(str(assertionFile), str(testFolder))

    assert expectedRules == actualRules
    printErrorMock.assert_called_once_with(expectedErrorMessage)

def test_getRestOfLineWithSpacesStartingWithToken_shouldGetRestOfLineWithSpaces():
    inputLine = "someRuleName someConst this  is   the     rest of the line"
    tokens = inputLine.split()
    expected = "this  is   the     rest of the line"
    actual = assertion_file_parser.getRestOfLineWithSpacesStartingWithToken(2, tokens, inputLine)
    assert actual == expected

def test_parseAssertionFile_shouldReturnAssertionRuleArray():
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    testFolder = Path(currentFolder).parent.joinpath("example")
    assertionFile = testFolder.joinpath("sampleAssertionFileWithVisibleWhitespace.yaml")
    options = {VISIBLE_WHITESPACE : True}

    expectedRules = []
    expectedRules.append(PathExistsRule(options, str(testFolder), "foo.txt"))
    expectedRules.append(PathExistsRule(options, str(testFolder), "bin"))
    expectedRules.append(PathNotExistsRule(options, str(testFolder), "missingFile"))
    expectedRules.append(FileMatchesRule(options, str(testFolder), "build.gradle", "expectedBuild.gradle"))
    expectedRules.append(RunScriptRule(options, str(testFolder), "MyApp", "./gradlew clean build"))
    expectedRules.append(FileContainsLineRule(options, str(testFolder), "MyApp/foo", "this line should exist"))
    expectedRules.append(FileDoesNotContainLineRule(options, str(testFolder), "MyApp/foo", "this line should not exist"))
    expectedRules.append(FileHasRegexMatchLineRule(options, str(testFolder), "MyApp/foo", "^lo+king \\sfor.*$"))
    expectedRules.append(FileDoesNotRegexMatchRule(options, str(testFolder), "MyApp/foo", "^lo+king\\s[fdfgd]{4} or.*$"))
    expectedRules.append(FileContainsSnippetRule(options, str(testFolder), "MyApp/foo", "goodSnippet.txt"))
    expectedRules.append(FileDoesNotContainSnippetRule(options, str(testFolder), "MyApp/foo", "badSnippet.txt"))

    actualRules = assertion_file_parser.parseAssertionFile(str(assertionFile), str(testFolder))

    assert expectedRules == actualRules