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

from cookiecutterassert import cookie_cutter_interface
from cookiecutterassert import assertion_file_parser
import os.path
from cookiecutterassert import messager

def getConfigFile(testFolder):
    configFile = testFolder+"/config.yaml"
    if not os.path.isfile(configFile):
        configFile = testFolder+"/config.yml"
    return configFile

def getDefaultConfigFile(templateFolder):
    configFile = templateFolder+"/defaultConfig.yaml"
    if not os.path.isfile(configFile):
        configFile = templateFolder+"/defaultConfig.yml"
    return configFile

def getAssertionsFile(testFolder):
    assertionsFile = testFolder+"/assertions.yaml"
    if not os.path.isfile(assertionsFile):
        assertionsFile = testFolder+"/assertions.yml"
    return assertionsFile

def executeAllTestsInFolder(templateFolder, testFolder):
    messager.printMessage("---Starting tests for "+testFolder)
    outputFolder = testFolder+"/build"
    configFile = getConfigFile(testFolder)
    defaultConfigFile = getDefaultConfigFile(templateFolder)
    assertionsFile = getAssertionsFile(testFolder)
    cookie_cutter_interface.generateFilesFromTemplate(templateFolder, configFile, outputFolder, defaultConfigFile)
    
    rules = assertion_file_parser.parseAssertionFile(assertionsFile, testFolder)
    if (len(rules) == 0):
        messager.printError("ERROR: No assertions found in test folder: {}".format(testFolder))
        return False

    ruleResult = True
    for rule in rules:
        ruleResult = rule.execute(outputFolder)
        if not ruleResult:
            break
    return ruleResult
