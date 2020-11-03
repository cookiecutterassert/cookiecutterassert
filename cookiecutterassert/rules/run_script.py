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

import os.path
import subprocess
from cookiecutterassert import messager

class RunScriptRule:

    def __init__(self, options, testFolder, runFolder, script):
        self.script = script
        self.runFolder = runFolder
        self.testFolder = testFolder
        self.options = options

    def execute(self, outputFolder):
        workingDir = str(os.path.join(outputFolder, self.runFolder))

        scriptprocess = subprocess.Popen(self.script, cwd = workingDir, shell=True)
        scriptprocess.wait()
        success = scriptprocess.returncode == 0
        if (not success):
            errorMessage = "assertion runScript {} {} failed.  with non-zero return code [{}]".format(self.runFolder, self.script, scriptprocess.returncode)
            messager.printError(errorMessage)
        return success
    
    def __eq__(self, obj):
        return isinstance(obj, RunScriptRule) \
            and obj.script == self.script \
            and obj.runFolder == self.runFolder \
            and obj.testFolder == self.testFolder \
            and obj.options == self.options

    def __ne__(self, obj):
        return not self == obj

    def __str__(self):
        return "{0}: [testFolder={1}, runFolder={2}, script={3}, options={4}]".format(type(self).__name__, self.testFolder, self.runFolder, self.script, self.options)

    def __repr__(self):
        return self.__str__()