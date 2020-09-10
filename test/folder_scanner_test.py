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

from cookiecutterassert import folder_scanner
import os
import os.path
from unittest.mock import patch
from pathlib import Path

def test_findAllTestFolders_shouldReturnAListOfAllFoldersThatHaveTestConfigs():
    testFolder = os.path.dirname(os.path.abspath(__file__))
    fixturePath = Path(testFolder).parent.joinpath("example").joinpath("dirTreeWithTests")
    test0Path = fixturePath.joinpath("test0")
    test1Path = fixturePath.joinpath("otherFolder").joinpath("test1")
    test2Path = fixturePath.joinpath("otherFolder").joinpath("test2")
    
    expected = {str(test0Path), str(test1Path), str(test2Path)}
    actual = folder_scanner.findAllTestFolders(str(fixturePath))

    assert actual == expected


@patch('os.listdir')
@patch('os.path.isfile')
def test_isTestFolder_shouldReturnTrueIfFolderHasAssertionsAndConfig(isFileMock, listDirMock):
    fileList = [ "assertions.yaml", "config.yaml", "other.txt"]
    folder = "/foo/bar"
    listDirMock.return_value=fileList
    isFileMock.return_value = True
    
    actual = folder_scanner.isTestFolder(folder)
    assert actual == True


@patch('os.listdir')
@patch('os.path.isfile')
def test_isTestFolder_shouldReturnTrueIfFolderHasAssertionsYmlAndConfigYaml(isFileMock, listDirMock):
    fileList = [ "assertions.yml", "config.yaml", "other.txt"]
    folder = "/foo/bar"
    listDirMock.return_value=fileList
    isFileMock.return_value = True
    
    actual = folder_scanner.isTestFolder(folder)
    assert actual == True


@patch('os.listdir')
@patch('os.path.isfile')
def test_isTestFolder_shouldReturnTrueIfFolderHasAssertionsYamlAndConfigYml(isFileMock, listDirMock):
    fileList = [ "assertions.yaml", "config.yml", "other.txt"]
    folder = "/foo/bar"
    listDirMock.return_value=fileList
    isFileMock.return_value = True
    
    actual = folder_scanner.isTestFolder(folder)
    assert actual == True


@patch('os.listdir')
@patch('os.path.isfile')
def test_isTestFolder_shouldReturnTrueIfFolderHasAssertionsYmlAndConfigYml(isFileMock, listDirMock):
    fileList = [ "assertions.yml", "config.yml", "other.txt"]
    folder = "/foo/bar"
    listDirMock.return_value=fileList
    isFileMock.return_value = True
    
    actual = folder_scanner.isTestFolder(folder)
    assert actual == True


@patch('os.listdir')
@patch('os.path.isfile')
def test_isTestFolder_shouldReturnFalseIfNoAssertions(isFileMock, listDirMock):
    fileList = [ "config.yaml", "other.txt"]
    folder = "/foo/bar"
    listDirMock.return_value=fileList
    isFileMock.return_value = True
    
    actual = folder_scanner.isTestFolder(folder)
    assert actual == False


@patch('os.listdir')
@patch('os.path.isfile')
def test_isTestFolder_shouldReturnFalseIfNoConfig(isFileMock, listDirMock):
    fileList = ["assertions.yaml", "other.txt"]
    folder = "/foo/bar"
    listDirMock.return_value=fileList
    isFileMock.return_value = True
    
    actual = folder_scanner.isTestFolder(folder)
    assert actual == False

@patch('os.listdir')
@patch('os.path.isfile')
def test_isTestFolder_shouldReturnFalseIfAssertionsIsFolder(isFileMock, listDirMock):
    fileList = ["assertions.yaml", "other.txt", "config.yaml"]
    folder = "/foo/bar"

    def isFile_side_effect(fileName):
        return fileName != os.path.join(folder, "assertions.yaml")

    listDirMock.return_value=fileList
    isFileMock.side_effect = isFile_side_effect
    
    actual = folder_scanner.isTestFolder(folder)
    assert actual == False

@patch('os.listdir')
@patch('os.path.isfile')
def test_isTestFolder_shouldReturnFalseIfConfigIsFolder(isFileMock, listDirMock):
    fileList = ["assertions.yaml", "other.txt", "config.yaml"]
    folder = "/foo/bar"

    def isFile_side_effect(fileName):
        return fileName != os.path.join(folder, "config.yaml")

    listDirMock.return_value=fileList
    isFileMock.side_effect = isFile_side_effect
    
    actual = folder_scanner.isTestFolder(folder)
    assert actual == False
