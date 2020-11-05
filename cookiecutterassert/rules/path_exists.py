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
from cookiecutterassert import messager

class PathExistsRule:

    def __init__(self, options, testFolder, pathName):
        self.pathName = pathName
        self.testFolder = testFolder
        self.options = options

    def execute(self, outputFolder):
        success = os.path.exists(os.path.join(outputFolder, self.pathName))
        if (not success):
            messager.printError("assertion pathExists "+self.pathName+" failed.  Cannot locate path "+os.path.join(outputFolder, self.pathName))
        return success
    
    def __eq__(self, obj):
        return isinstance(obj, PathExistsRule) \
            and obj.pathName == self.pathName \
            and obj.testFolder == self.testFolder \
            and obj.options == self.options

    def __ne__(self, obj):
        return not self == obj

    def __str__(self):
        return "{0}: [testFolder={1}, pathName={2}, options={3}]".format(type(self).__name__, self.testFolder, self.pathName, self.options)

    def __repr__(self):
        return self.__str__()