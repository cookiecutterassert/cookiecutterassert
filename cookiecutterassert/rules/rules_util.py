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

from genericpath import exists
import os.path
from pathlib import Path

def readLinesFromFile(fileName, folder = None, removeNewline = True):
    fileNameWithPath = fileName
    if (folder != None):
        fileNameWithPath = os.path.join(folder, fileName)
    
    fileHandle = open(fileNameWithPath, 'rb')
    myBytes = fileHandle.read()
    fileHandle.close()
    fileString = myBytes.decode("utf-8")
    fileLines = fileString.split("\n")

    withoutNewlines = []
    for line in fileLines:
        if(not removeNewline and line != fileLines[-1]):
            line = line+"\n"
        withoutNewlines.append(line)

    return withoutNewlines

def snippetExistsInFile(snippetLines, fileLines):
    if len(snippetLines) > len(fileLines):
        return False
    for i in range(0, len(fileLines) - len(snippetLines) + 1):
        if fileLines[i:i+len(snippetLines)] == snippetLines:
            return True
    return False

def path_exists_case_sensitive(path, parent_path = ""):
    if (parent_path != ""):
        fullOSPath = os.path.join(parent_path, path)
    else:
        fullOSPath  = path
        
    fullPath = Path(fullOSPath)
    if (not fullPath.exists()):
        return False
        
    currentPath = fullPath.resolve()
    i = 0
    while (currentPath != currentPath.parent):
        found = False
        for child in currentPath.parent.iterdir():
            if (child.name == currentPath.name):
                found = True
        if (not found):
            return False
        currentPath = currentPath.parent
    return True