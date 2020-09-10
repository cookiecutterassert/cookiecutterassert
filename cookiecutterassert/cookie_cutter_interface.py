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

from cookiecutter import generate
import yaml
import shutil
import os

def loadYamlFile(yamlFile):
    if (os.path.exists(yamlFile)):
        with open(yamlFile, 'r') as yamlConfigFile:
            loadedContext = yaml.load(yamlConfigFile, Loader=yaml.FullLoader)
            if (loadedContext is None 
                or len(loadedContext) == 0
                or loadedContext['default_context'] is None):
                return {'default_context': {} }
            return loadedContext
    return {'default_context': {} }

def loadCookieCutterContext(configfile, defaultConfigFile):
    cookiecutterContext = {}
    context = {}
    cookiecutterContext['cookiecutter'] = loadYamlFile(defaultConfigFile)['default_context']
    cookiecutterContext['cookiecutter'].update(loadYamlFile(configfile)['default_context'])
    return cookiecutterContext


def eraseFolder(folder):
    if (os.path.exists(folder)):
        shutil.rmtree(folder)
    os.mkdir(folder)

def generateFilesFromTemplate(template, configfile, output, defaultConfigFile):
    cookiecutterContext = loadCookieCutterContext(configfile, defaultConfigFile)
    eraseFolder(output)
    generate.generate_files(repo_dir=template, context=cookiecutterContext, output_dir=output)
