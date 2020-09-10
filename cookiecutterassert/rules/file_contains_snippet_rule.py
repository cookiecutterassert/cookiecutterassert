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

from cookiecutterassert.rules.rules_util import readLinesFromFile, snippetExistsInFile
from cookiecutterassert import messager
import os

class FileContainsSnippetRule:

    def __init__(self, testFolder, fileName, snippetFile):
        self.snippetFile = snippetFile
        self.fileName = fileName
        self.testFolder = testFolder

    def execute(self, outputFolder):
        if (not os.path.exists(os.path.join(outputFolder, self.fileName))):
            messager.printError("assertion fileContainsSnippet {0} {1} failed. {0} does not exist in {2}.".format(self.fileName, self.snippetFile, outputFolder))
            return False
        if (not os.path.exists(os.path.join(self.testFolder, self.snippetFile))):
            messager.printError("assertion fileContainsSnippet {0} {1} failed. {1} does not exist in {2}.".format(self.fileName, self.snippetFile, self.testFolder))
            return False
        fileLines = readLinesFromFile(self.fileName, folder=outputFolder)
        snippetLines = readLinesFromFile(self.snippetFile, folder=self.testFolder)
        success = snippetExistsInFile(snippetLines, fileLines)
        if not success:
            messager.printError("assertion fileContainsSnippet {0} {1} failed.  Matching lines from {1} not found in {2}/{0}.".format(self.fileName, self.snippetFile, outputFolder))
        return success
    
    def __eq__(self, obj):
        return isinstance(obj, FileContainsSnippetRule) \
            and obj.snippetFile == self.snippetFile \
            and obj.fileName == self.fileName \
            and obj.testFolder == self.testFolder

    def __ne__(self, obj):
        return not self == obj

    def __str__(self):
        return "{0}: [testFolder={1}, fileName={2}, snippetFile={3}]".format(type(self).__name__, self.testFolder, self.fileName, self.snippetFile)

    def __repr__(self):
        return self.__str__()
    
