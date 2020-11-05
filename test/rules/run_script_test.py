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

from cookiecutterassert.rules.run_script import RunScriptRule
from unittest.mock import patch
import subprocess
import os.path

outputFolder = "someoutput/build"
testFolder = "someoutput"
runFolder = "runFolder"
script = "myExecubtable arg0 arg1"

class FakeProcess:
    def __init__(self, expectedReturnCode):
        self.returncode = None
        self.expectedReturnCode = expectedReturnCode

    def wait(self):
        self.returncode = self.expectedReturnCode

@patch("subprocess.Popen")
def test_execute_shouldRunScriptAndReturnTrueIfTheScriptSucceeds(mockPopen):
    mockProcess = FakeProcess(0)
    mockPopen.return_value = mockProcess
    expectedWorkingDir = str(os.path.join(outputFolder, runFolder))

    runScriptRule = RunScriptRule({}, testFolder, runFolder, script)
    assert runScriptRule.execute(outputFolder)
    mockPopen.assert_called_once_with(script, cwd=expectedWorkingDir, shell=True);

@patch("cookiecutterassert.messager.printError")
@patch("subprocess.Popen")
def test_execute_shouldRunScriptAndReturnFalseAndPrintMessageIfTheScriptFails(mockPopen, mockPrint):
    mockProcess = FakeProcess(1)
    mockPopen.return_value = mockProcess
    expectedWorkingDir = str(os.path.join(outputFolder, runFolder))
    expectedErrorMessage = "assertion runScript {} {} failed.  with non-zero return code [{}]".format(runFolder, script, mockProcess.expectedReturnCode)

    runScriptRule = RunScriptRule({}, testFolder, runFolder, script)
    assert runScriptRule.execute(outputFolder) == False
    mockPopen.assert_called_once_with(script, cwd=expectedWorkingDir, shell=True);
    mockPrint.assert_called_once_with(expectedErrorMessage)