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
from unittest.mock import patch
from unittest.mock import mock_open
from cookiecutter.generate import generate_files

fakeTemplate = 'template'

@patch('yaml.load')
@patch("os.path.exists")
def test_loadYaml_shouldLoadFromYamlFile(mockexists, mockYamlLoad):
   fake_yaml_context = {'default_context': { "foo": "bar"}}
   fake_config_file = 'README.md'
   mockexists.return_value = True

   mockYamlLoad.return_value = fake_yaml_context
   mockOpen = mock_open(read_data=fake_config_file)
   with patch('__main__.open', mockOpen):
         
      actual = cookie_cutter_interface.loadYamlFile(fake_config_file)
      assert actual == fake_yaml_context

@patch("os.path.exists")
def test_loadYaml_shouldReturnEmptyDefaultContextIfNotExists(mockexists):
   fake_config_file = 'README.md'
   mockexists.return_value = False

   actual = cookie_cutter_interface.loadYamlFile(fake_config_file)
   assert actual == {'default_context': {} }
   mockexists.assert_called_once_with(fake_config_file)

@patch('yaml.load')
@patch("os.path.exists")
def test_loadYaml_shouldReturnEmptyDefaultContextIfEmptyYaml(mockexists, mockYamlLoad):
   fake_yaml_context = {}
   fake_config_file = 'README.md'
   mockexists.return_value = True

   mockYamlLoad.return_value = fake_yaml_context
   mockOpen = mock_open(read_data=fake_config_file)
   with patch('__main__.open', mockOpen):
         
      actual = cookie_cutter_interface.loadYamlFile(fake_config_file)
      assert actual == {'default_context': {} }

@patch('yaml.load')
@patch("os.path.exists")
def test_loadYaml_shouldReturnEmptyDefaultContextIfNone(mockexists, mockYamlLoad):
   fake_config_file = 'README.md'
   mockexists.return_value = True

   mockYamlLoad.return_value = None
   mockOpen = mock_open(read_data=fake_config_file)
   with patch('__main__.open', mockOpen):
         
      actual = cookie_cutter_interface.loadYamlFile(fake_config_file)
      assert actual == {'default_context': {} }

@patch('yaml.load')
@patch("os.path.exists")
def test_loadYaml_shouldReturnEmptyDefaultContextDefaultContextIsNone(mockexists, mockYamlLoad):
   fake_yaml_context = {'default_context': None}
   fake_config_file = 'README.md'
   mockexists.return_value = True

   mockYamlLoad.return_value = fake_yaml_context
   mockOpen = mock_open(read_data=fake_config_file)
   with patch('__main__.open', mockOpen):
         
      actual = cookie_cutter_interface.loadYamlFile(fake_config_file)
      assert actual == {'default_context': {} }

@patch('cookiecutterassert.cookie_cutter_interface.loadYamlFile')
def test_loadCookieCutterContext_shouldLoadFromYamlFile(mockYamlLoad):
   fake_yaml_context = { "foo": "bar"}
   fake_config_file = 'README.md'

   mockYamlLoad.return_value = { "default_context": fake_yaml_context }
         
   actual = cookie_cutter_interface.loadCookieCutterContext(fake_config_file, fakeTemplate)
   assert actual["cookiecutter"] == fake_yaml_context
   
@patch('cookiecutterassert.cookie_cutter_interface.loadYamlFile')
def test_loadCookieCutterContext_shouldCombineDefaultYamlFile(mockYamlLoad):
   fake_yaml_context = { "foo": "bar"}
   default_yaml_context  = {"blue": "green"}
   combined_yaml_context = {"blue": "green", "foo": "bar"}
   fake_config_file = 'README.md'
   fake_default_config_file = fakeTemplate+'/config.yaml'

   def fakeLoad(yamlFile):
      if (yamlFile == fake_config_file):
         return { "default_context": fake_yaml_context }
      elif (yamlFile == fake_default_config_file):
         return { "default_context": default_yaml_context }
      else:
          return None
   mockYamlLoad.side_effect = fakeLoad
         
   actual = cookie_cutter_interface.loadCookieCutterContext(fake_config_file, fake_default_config_file)
   assert actual["cookiecutter"] == combined_yaml_context

@patch('os.path.exists')
@patch('shutil.rmtree')
@patch('os.mkdir')
def test_eraseFolder_shouldDeleteAndRemakeTheFolder(mock_mkdir, mock_rmtree, mock_exists):
   fake_folder = 'foo'
   mock_exists.return_value = True

   cookie_cutter_interface.eraseFolder(fake_folder)
   
   mock_rmtree.assert_called_once_with('foo')
   mock_mkdir.assert_called_once_with('foo')

@patch('os.path.exists')
@patch('shutil.rmtree')
@patch('os.mkdir')
def test_eraseFolder_shouldNotDeleteFolderIfNotExists(mock_mkdir, mock_rmtree, mock_exists):
   fake_folder = 'foo'
   mock_exists.return_value = False


   cookie_cutter_interface.eraseFolder(fake_folder)
   
   mock_rmtree.assert_not_called()
   mock_mkdir.assert_called_once_with('foo')

@patch('cookiecutter.generate.generate_files')
@patch('cookiecutterassert.cookie_cutter_interface.eraseFolder')
@patch('cookiecutterassert.cookie_cutter_interface.loadCookieCutterContext')
def test_generateFilesFromTemplate_shouldLoadContextDeleteOldFilesAndRegenerate(fakeLoadContext, fakeEraseFolder, fakeGenerateFiles):
   fake_yaml_context = { "foo": "bar"}
   defaultConfigFile = "defaultConfigFile.yaml"
   fakeLoadContext.return_value = fake_yaml_context
   
   fakeFolder='foo'

   cookie_cutter_interface.generateFilesFromTemplate(fakeTemplate, fake_yaml_context, fakeFolder, defaultConfigFile)

   fakeEraseFolder.assert_called_once_with(fakeFolder)
   fakeGenerateFiles.assert_called_once_with(repo_dir=fakeTemplate, context=fake_yaml_context, output_dir=fakeFolder)
   fakeLoadContext.assert_called_once_with(fake_yaml_context, defaultConfigFile)