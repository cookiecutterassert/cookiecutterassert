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

from cookiecutter.main import cookiecutter
import yaml
import shutil
import os


def load_yaml_file(yaml_file):
    if os.path.exists(yaml_file):
        with open(yaml_file, 'r') as yamlConfigFile:
            loaded_context = yaml.load(yamlConfigFile, Loader=yaml.FullLoader)
            if (loaded_context is None
                    or len(loaded_context) == 0
                    or loaded_context['default_context'] is None):
                return {'default_context': {}}
            return loaded_context
    return {'default_context': {}}


def load_cookiecutter_context(config_file, default_config_file):
    cookiecutter_context = load_yaml_file(default_config_file)['default_context']
    cookiecutter_context.update(load_yaml_file(config_file)['default_context'])
    return cookiecutter_context


def erase_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


def generateFilesFromTemplate(template, config_file, output, default_config_file):
    cookiecutter_context = load_cookiecutter_context(config_file, default_config_file)
    erase_folder(output)
    cookiecutter(template=template,
                 no_input=True,
                 overwrite_if_exists=True,
                 extra_context=cookiecutter_context,
                 output_dir=output)
