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

import os
from pathlib import Path
from cookiecutterassert.rules.rules_util import readLinesFromFile, path_exists_case_sensitive

expectedLines = [
    "line0",
    "line1",
    "looking for this line",
    "line2"
]

def test_readLinesFromFile_shouldReadLinesFromFile():
    assert readLinesFromFile("fileWithLine.txt", folder="example") == expectedLines

def test_readLinesFromFile_shouldReadLinesFromFQPath():
    assert readLinesFromFile("example/fileWithLine.txt") == expectedLines

def test_readLinesFromFile_shouedPreserveNewlinesIfAsked():
    expectedLinesWithNewlines = []
    for line in expectedLines:
        expectedLinesWithNewlines.append(line+"\n")
    expectedLinesWithNewlines[-1] = expectedLines[-1]
    assert readLinesFromFile("fileWithLine.txt", folder="example", removeNewline=False) == expectedLinesWithNewlines

def test_path_exists_case_sensitive_returns_true_for_existing_path():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    output_folder = Path(current_folder).parent.parent
    test_folder = str(output_folder)
    path_name = "example/dirTreeWithTests/otherFolder/test1"

    assert path_exists_case_sensitive(path_name, parent_path=test_folder) == True
    

def test_path_exists_case_sensitive_returns_false_for_non_existing_path():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    output_folder = Path(current_folder).parent.parent
    test_folder = str(output_folder)
    path_name0 = "example/dirTreeWithTests/2qffg88assh/test1"
    path_name1 = "example/asdhjgf67qbfa/otherFolder/test1"
    path_name2 = "example/dirTreeWithTests/otherFolder/sd68asd6"

    assert path_exists_case_sensitive(path_name0, parent_path=test_folder) == False
    assert path_exists_case_sensitive(path_name1, parent_path=test_folder) == False
    assert path_exists_case_sensitive(path_name2, parent_path=test_folder) == False

def test_path_exists_case_sensitive_returns_false_for_incorrect_case():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    output_folder = Path(current_folder).parent.parent
    test_folder = str(output_folder)
    path_name0 = "example/dirTreewithTests/otherFolder/test1"
    path_name1 = "example/dirTreeWithTests/otherfolder/test1"
    path_name2 = "example/dirTreeWithTests/otherFolder/tEst1"

    assert path_exists_case_sensitive(path_name0, parent_path=test_folder) == False
    assert path_exists_case_sensitive(path_name1, parent_path=test_folder) == False
    assert path_exists_case_sensitive(path_name2, parent_path=test_folder) == False

def test_path_exists_case_sensitive_returns_true_for_existing_path_no_parent():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    output_folder = Path(current_folder).parent.parent
    test_folder = str(output_folder)
    path_name = os.path.join(test_folder, "example/dirTreeWithTests/otherFolder/test1")

    assert path_exists_case_sensitive(path_name) == True

def test_path_exists_case_sensitive_returns_false_for_incorrect_case_with_not_parent():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    output_folder = Path(current_folder).parent.parent
    test_folder = str(output_folder)
    path_name0 = os.path.join(test_folder, "example/dirTreewithTests/otherFolder/test1")
    path_name1 = os.path.join(test_folder, "example/dirTreeWithTests/otherfolder/test1")
    path_name2 = os.path.join(test_folder, "example/dirTreeWithTests/otherFolder/tEst1")

    assert path_exists_case_sensitive(path_name0) == False
    assert path_exists_case_sensitive(path_name1) == False
    assert path_exists_case_sensitive(path_name2) == False

