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

fake_template = 'template'


@patch('yaml.load')
@patch("os.path.exists")
def test_load_yaml_file_should_load_from_yaml_file(mock_exists, mock_yaml_load):
    fake_yaml_context = {'default_context': {"foo": "bar"}}
    fake_config_file = 'README.md'
    mock_exists.return_value = True

    mock_yaml_load.return_value = fake_yaml_context
    fake_open = mock_open(read_data=fake_config_file)
    with patch('__main__.open', fake_open):
        actual = cookie_cutter_interface.load_yaml_file(fake_config_file)
        assert actual == fake_yaml_context


@patch("os.path.exists")
def test_load_yaml_file_shouldReturnEmptyDefaultContextIfNotExists(mock_exists):
    fake_config_file = 'README.md'
    mock_exists.return_value = False

    actual = cookie_cutter_interface.load_yaml_file(fake_config_file)
    assert actual == {'default_context': {}}
    mock_exists.assert_called_once_with(fake_config_file)


@patch('yaml.load')
@patch("os.path.exists")
def test_load_yaml_file_shouldReturnEmptyDefaultContextIfEmptyYaml(mockexists, mockYamlLoad):
    fake_yaml_context = {}
    fake_config_file = 'README.md'
    mockexists.return_value = True

    mockYamlLoad.return_value = fake_yaml_context
    mockOpen = mock_open(read_data=fake_config_file)
    with patch('__main__.open', mockOpen):
        actual = cookie_cutter_interface.load_yaml_file(fake_config_file)
        assert actual == {'default_context': {}}


@patch('yaml.load')
@patch("os.path.exists")
def test_load_yaml_file_shouldReturnEmptyDefaultContextIfNone(mockexists, mockYamlLoad):
    fake_config_file = 'README.md'
    mockexists.return_value = True

    mockYamlLoad.return_value = None
    mockOpen = mock_open(read_data=fake_config_file)
    with patch('__main__.open', mockOpen):
        actual = cookie_cutter_interface.load_yaml_file(fake_config_file)
        assert actual == {'default_context': {}}


@patch('yaml.load')
@patch("os.path.exists")
def test_load_yaml_file_shouldReturnEmptyDefaultContextDefaultContextIsNone(mockexists, mockYamlLoad):
    fake_yaml_context = {'default_context': None}
    fake_config_file = 'README.md'
    mockexists.return_value = True

    mockYamlLoad.return_value = fake_yaml_context
    mockOpen = mock_open(read_data=fake_config_file)
    with patch('__main__.open', mockOpen):
        actual = cookie_cutter_interface.load_yaml_file(fake_config_file)
        assert actual == {'default_context': {}}


@patch('cookiecutterassert.cookie_cutter_interface.load_yaml_file')
def test_loadCookieCutterContext_shouldLoadFromYamlFile(mockYamlLoad):
    fake_yaml_context = {"foo": "bar"}
    fake_config_file = 'README.md'

    mockYamlLoad.return_value = {"default_context": fake_yaml_context}

    actual = cookie_cutter_interface.load_cookiecutter_context(fake_config_file, fake_template)
    assert actual == fake_yaml_context


@patch('cookiecutterassert.cookie_cutter_interface.load_yaml_file')
def test_load_cookiecutter_context_shouldCombineDefaultYamlFile(mockYamlLoad):
    fake_yaml_context = {"foo": "bar"}
    default_yaml_context = {"blue": "green"}
    combined_yaml_context = {"blue": "green", "foo": "bar"}
    fake_config_file = 'README.md'
    fake_default_config_file = fake_template + '/config.yaml'

    def fakeLoad(yamlFile):
        if (yamlFile == fake_config_file):
            return {"default_context": fake_yaml_context}
        elif (yamlFile == fake_default_config_file):
            return {"default_context": default_yaml_context}
        else:
            return None

    mockYamlLoad.side_effect = fakeLoad

    actual = cookie_cutter_interface.load_cookiecutter_context(fake_config_file, fake_default_config_file)
    assert actual == combined_yaml_context


@patch('os.path.exists')
@patch('shutil.rmtree')
@patch('os.mkdir')
def test_erase_folder_shouldDeleteAndRemakeTheFolder(mock_mkdir, mock_rmtree, mock_exists):
    fake_folder = 'foo'
    mock_exists.return_value = True

    cookie_cutter_interface.erase_folder(fake_folder)

    mock_rmtree.assert_called_once_with('foo')
    mock_mkdir.assert_called_once_with('foo')


@patch('os.path.exists')
@patch('shutil.rmtree')
@patch('os.mkdir')
def test_erase_folder_shouldNotDeleteFolderIfNotExists(mock_mkdir, mock_rmtree, mock_exists):
    fake_folder = 'foo'
    mock_exists.return_value = False

    cookie_cutter_interface.erase_folder(fake_folder)

    mock_rmtree.assert_not_called()
    mock_mkdir.assert_called_once_with('foo')


@patch('cookiecutterassert.cookie_cutter_interface.cookiecutter')
@patch('cookiecutterassert.cookie_cutter_interface.erase_folder')
@patch('cookiecutterassert.cookie_cutter_interface.load_cookiecutter_context')
def test_generateFilesFromTemplate_shouldLoadContextDeleteOldFilesAndRegenerate(fake_load_context, fake_erase_folder,
                                                                                fake_cookiecutter):
    fake_yaml_context = {"foo": "bar"}
    default_config_file = "defaultConfigFile.yaml"
    fake_load_context.return_value = fake_yaml_context

    fake_folder = 'foo'

    cookie_cutter_interface.generateFilesFromTemplate(fake_template, fake_yaml_context, fake_folder, default_config_file)

    fake_erase_folder.assert_called_once_with(fake_folder)
    fake_cookiecutter.assert_called_once_with(template=fake_template,
                                              no_input=True,
                                              overwrite_if_exists=True,
                                              extra_context=fake_yaml_context,
                                              output_dir=fake_folder)
    fake_load_context.assert_called_once_with(fake_yaml_context, default_config_file)
