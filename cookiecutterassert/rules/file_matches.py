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

import filecmp
import os.path
from cookiecutterassert import messager
from cookiecutterassert.rules import rules_util
import difflib
import click

from cookiecutterassert.rules.option_names import VISIBLE_WHITESPACE

class FileMatchesRule:

    def __init__(self, options, testFolder, fileName, fixturePath):
        self.fileName = fileName
        self.fixturePath = fixturePath
        self.testFolder = testFolder
        self.options = options

    def execute(self, outputFolder):
        fixtureFile = os.path.join(self.testFolder, self.fixturePath)
        outputFile = os.path.join(outputFolder, self.fileName)
        if (not rules_util.path_exists_case_sensitive(fixtureFile)):
            messager.printError("assertion fileMatches "+ self.fileName+" "+self.fixturePath +" failed.  "+os.path.abspath(os.path.join(self.testFolder, self.fixturePath))+" does not exist")
            return False
        if (not rules_util.path_exists_case_sensitive(outputFile)):
            messager.printError("assertion fileMatches "+ self.fileName+" "+self.fixturePath +" failed.  "+os.path.abspath(os.path.join(outputFolder, self.fileName))+" does not exist")
            return False
        success = filecmp.cmp(outputFile, fixtureFile, shallow=False)
        if (not success):
            messager.printError("assertion fileMatches "+self.fileName+" "+self.fixturePath +" failed.  Files differ")
            self.printDifferences(outputFile, fixtureFile)
        return success
    
    def printDifferences(self, outputFile, fixtureFile):
        try:
            outputLines = rules_util.readLinesFromFile(outputFile, removeNewline=False)
            fixtureLines = rules_util.readLinesFromFile(fixtureFile, removeNewline=False)
            i = 0
            for diffLine in difflib.unified_diff(outputLines, fixtureLines, fromfile=outputFile, tofile=fixtureFile):
                if (i > 2):
                    diffLine = self.getVisibleWhitespace(diffLine)
                styledLine = diffLine
                if (diffLine.startswith("+")):
                    styledLine = click.style(diffLine, fg='blue')
                elif (diffLine.startswith("-")):
                    styledLine = click.style(diffLine, fg="yellow")
                click.echo(styledLine)
                i = i+1
        except UnicodeDecodeError:
            messager.printError("One or both files are binary, unable to print differences")

    def __eq__(self, obj):
        return isinstance(obj, FileMatchesRule) \
            and obj.fileName == self.fileName \
            and obj.fixturePath == self.fixturePath \
            and obj.testFolder == self.testFolder \
            and obj.options == self.options

    def __ne__(self, obj):
        return not self == obj

    def __str__(self):
        return "{0}: [testFolder={1}, fileName={2}, fixturePath={3}, options={4}]".format(type(self).__name__, self.testFolder, self.fileName, self.fixturePath, self.options)

    def __repr__(self):
        return self.__str__()
    
    def getVisibleWhitespace(self, diffLine):
        if (VISIBLE_WHITESPACE in self.options and self.options[VISIBLE_WHITESPACE]):
            first_char = diffLine[0:1]
            diff_body = diffLine[1:]
            updated_body = diff_body.replace(" ", "•").replace("\t","→").replace("\n", "¶").replace("\r", "↵")
            return first_char + updated_body
        else:
            return  diffLine.replace("\n", "")