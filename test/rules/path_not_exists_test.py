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

from cookiecutterassert.rules.path_not_exists import PathNotExistsRule
from unittest.mock import patch
import os.path

@patch("cookiecutterassert.rules.rules_util.path_exists_case_sensitive")
@patch("cookiecutterassert.messager.printError")
def test_execute_shouldReturnFalseIfTHePathExists(printMock, existsMock):
    existsMock.return_value=True;
    fileName = "some/test/file"
    outputFolder = "/someoutput/build"
    
    pathNotExistsRule = PathNotExistsRule({}, "ignore", fileName)
    assert not pathNotExistsRule.execute(outputFolder)
    existsMock.assert_called_once_with(fileName, parent_path=outputFolder)
    printMock.assert_called_once_with("assertion pathNotExists "+fileName+" failed.  path "+os.path.join(outputFolder, fileName)+" exists")

@patch("cookiecutterassert.rules.rules_util.path_exists_case_sensitive")
def test_execute_shouldReturnTrueIfThePathDoesNotExist(existsMock):
    existsMock.return_value=False;
    fileName = "some/test/file"
    outputFolder = "/someoutput/build"
    
    pathNotExistsRule = PathNotExistsRule({}, "ignore", fileName)
    assert pathNotExistsRule.execute(outputFolder)

    