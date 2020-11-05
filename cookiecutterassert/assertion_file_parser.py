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

import yaml
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

def getRestOfLineWithSpacesStartingWithToken(startTokenIndex, tokens, line):
    charIndex = 0
    for tokenIndex in range(0, startTokenIndex):
        currentToken = tokens[tokenIndex]
        charIndex = line.index(currentToken, charIndex) + len(currentToken)
    charIndex = line.index(tokens[startTokenIndex], charIndex)
    return line[charIndex:]

def parseAssertionFile(assertionFile, testFolder, cli_options):
    rules = []
    with open(assertionFile, 'r') as yamlAssertionFile:
        assertionData = yaml.load(yamlAssertionFile, Loader=yaml.FullLoader)
        options = {}
        if ('options' in assertionData):
            options = assertionData['options']
        options.update(cli_options)
        for ruleString in assertionData["assertions"]:
            tokens = ruleString.split()
            if (tokens[0] == "pathExists"):
                rule = PathExistsRule(options, testFolder, tokens[1])
                rules.append(rule)
            elif (tokens[0] == "fileMatches"):
                rule = FileMatchesRule(options, testFolder, tokens[1], tokens[2])
                rules.append(rule)
            elif (tokens[0] == "pathNotExists"):
                rule = PathNotExistsRule(options, testFolder, tokens[1])
                rules.append(rule)
            elif (tokens[0] == "runScript"):
                script = getRestOfLineWithSpacesStartingWithToken(2, tokens, ruleString)
                rule = RunScriptRule(options, testFolder, tokens[1], script)
                rules.append(rule)
            elif (tokens[0] == "fileContainsLine"):
                line = getRestOfLineWithSpacesStartingWithToken(2, tokens, ruleString)
                rule = FileContainsLineRule(options, testFolder, tokens[1], line)
                rules.append(rule)
            elif (tokens[0] == "fileDoesNotContainLine"):
                line = getRestOfLineWithSpacesStartingWithToken(2, tokens, ruleString)
                rule = FileDoesNotContainLineRule(options, testFolder, tokens[1], line)
                rules.append(rule)
            elif (tokens[0] == "fileHasMatchingLine"):
                regex = getRestOfLineWithSpacesStartingWithToken(2, tokens, ruleString)
                rule = FileHasRegexMatchLineRule(options, testFolder, tokens[1], regex)
                rules.append(rule)
            elif (tokens[0] == "fileDoesNotHaveMatchingLine"):
                regex = getRestOfLineWithSpacesStartingWithToken(2, tokens, ruleString)
                rule = FileDoesNotRegexMatchRule(options, testFolder, tokens[1], regex)
                rules.append(rule)
            elif (tokens[0] == "fileContainsSnippet"):
                rule = FileContainsSnippetRule(options, testFolder, tokens[1], tokens[2])
                rules.append(rule)
            elif (tokens[0] == "fileDoesNotContainSnippet"):
                rule = FileDoesNotContainSnippetRule(options, testFolder, tokens[1], tokens[2])
                rules.append(rule)
            else:
                messager.printError("Unable to parse assertion file {}.  Error on assertion \"{}\"".format(assertionFile, ruleString))
                return []
    return rules