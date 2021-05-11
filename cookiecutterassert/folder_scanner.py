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

import os
from pathlib import Path




def isTestFolder(folder):
    fileNames = os.listdir(folder)
    return hasAssertionsFile(folder, fileNames) and hasConfigFile(folder, fileNames)

def hasAssertionsFile(folder, fileNames):
    return any(filter(lambda fileName: os.path.isfile(os.path.join(folder, fileName)) and isAssertionsFile(fileName),fileNames))

def isAssertionsFile(fileName):
    return fileName == "assertions.yaml" or fileName == "assertions.yml"

def hasConfigFile(folder, fileNames):
    return any(filter(lambda fileName: os.path.isfile(os.path.join(folder, fileName)) and isConfigFile(fileName),fileNames))

def isConfigFile(fileName):
    return fileName == "config.yaml" or fileName == "config.yml"


def recurseAddTestFolders(testFolderSet, folderPath):
    if (isTestFolder(str(folderPath))):
        testFolderSet.append(str(folderPath))
    else:
        for child in folderPath.iterdir():
            if (child.is_dir()):
                recurseAddTestFolders(testFolderSet, child)

def findAllTestFolders(parentFolder):
    testFolderSet = []
    parentPath = Path(parentFolder)
    recurseAddTestFolders(testFolderSet, parentPath)
    testFolderSet.sort()
    return testFolderSet
