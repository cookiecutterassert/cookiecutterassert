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

class FileMatchesRule:

    def __init__(self, testFolder, fileName, fixturePath):
        self.fileName = fileName
        self.fixturePath = fixturePath
        self.testFolder = testFolder

    def execute(self, outputFolder):
        fixtureFile = os.path.join(self.testFolder, self.fixturePath)
        outputFile = os.path.join(outputFolder, self.fileName)
        if (not os.path.exists(fixtureFile)):
            messager.printError("assertion fileMatches "+ self.fileName+" "+self.fixturePath +" failed.  "+os.path.abspath(os.path.join(self.testFolder, self.fixturePath))+" does not exist")
            return False
        if (not os.path.exists(outputFile)):
            messager.printError("assertion fileMatches "+ self.fileName+" "+self.fixturePath +" failed.  "+os.path.abspath(os.path.join(outputFolder, self.fileName))+" does not exist")
            return False
        success = filecmp.cmp(outputFile, fixtureFile, shallow=False)
        if (not success):
            messager.printError("assertion fileMatches "+self.fileName+" "+self.fixturePath +" failed.  Files differ")
            self.printDifferences(outputFile, fixtureFile)
        return success
    
    def printDifferences(self, outputFile, fixtureFile):
        try:
            outputLines = rules_util.readLinesFromFile(outputFile)
            fixtureLines = rules_util.readLinesFromFile(fixtureFile)
            for diffLine in difflib.unified_diff(outputLines, fixtureLines, fromfile=outputFile, tofile=fixtureFile):
                styledLine = diffLine
                if (diffLine.startswith("+")):
                    styledLine = click.style(diffLine, fg='blue')
                elif (diffLine.startswith("-")):
                    styledLine = click.style(diffLine, fg="yellow")
                click.echo(styledLine)
        except UnicodeDecodeError:
            messager.printError("One or both files are binary, unable to print differences")

    def __eq__(self, obj):
        return isinstance(obj, FileMatchesRule) \
            and obj.fileName == self.fileName \
            and obj.fixturePath == self.fixturePath \
            and obj.testFolder == self.testFolder

    def __ne__(self, obj):
        return not self == obj

    def __str__(self):
        return "{0}: [testFolder={1}, fileName={2}, fixturePath={3}]".format(type(self).__name__, self.testFolder, self.fileName, self.fixturePath)

    def __repr__(self):
        return self.__str__()