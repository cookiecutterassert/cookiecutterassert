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

from cookiecutterassert import folder_scanner
from cookiecutterassert import test_folder_executor

def runAllTestsInAllFolders(projectRootFolder):
    testFolders = folder_scanner.findAllTestFolders(projectRootFolder+'/test')
    allTestsPass = True
    for folder in testFolders :
        folderSuccess = test_folder_executor.executeAllTestsInFolder(projectRootFolder, folder)
        allTestsPass = allTestsPass and folderSuccess
    return allTestsPass