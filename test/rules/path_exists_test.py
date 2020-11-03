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

from cookiecutterassert.rules.path_exists import PathExistsRule
from unittest.mock import patch
import os.path

@patch("os.path.exists")
def test_execute_shouldReturnTrueIfTHePathExists(existsMock):
    existsMock.return_value=True;
    fileName = "some/test/file"
    outputFolder = "/someoutput/build"
    
    pathExistsRule = PathExistsRule({}, "ignore", fileName)
    assert pathExistsRule.execute(outputFolder)
    os.path.exists.assert_called_once_with(os.path.join(outputFolder, fileName))

@patch("os.path.exists")
@patch("cookiecutterassert.messager.printError")
def test_execute_shouldReturnFalseIfTHePathDoesNotExist(printMock, existsMock):
    existsMock.return_value=False;
    fileName = "some/test/file"
    outputFolder = "/someoutput/build"
    
    pathExistsRule = PathExistsRule({}, "ignore", fileName)
    assert not pathExistsRule.execute(outputFolder)
    printMock.assert_called_once_with("assertion pathExists "+fileName+" failed.  Cannot locate path "+os.path.join(outputFolder, fileName))