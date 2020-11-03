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

execute_test()
{
  EXPECTED_RESULT=$1
  shift;
  COMMAND=$@
  echo $COMMAND
  $COMMAND
  ACTUAL_RESULT=$?
  if [ $ACTUAL_RESULT != $EXPECTED_RESULT ] ; then
    echo "INTEGRATION TEST FAILED!!! expecting result of $EXPECTED_RESULT but got $ACTUAL_RESULT"
    exit 1
  fi
}

execute_test_expected_output()
{
  EXPECTED_RESULT=$1
  shift;
  FOLDER=$1
  shift;
  COMMAND=$@
  echo $COMMAND
  $COMMAND  > $FOLDER/actual-cookiecutterassert-output.txt
  ACTUAL_RESULT=$?
  if [ $ACTUAL_RESULT != $EXPECTED_RESULT ] ; then
    echo "INTEGRATION TEST FAILED!!! expecting result of $EXPECTED_RESULT but got $ACTUAL_RESULT"
    exit 1
  fi
  cmp $FOLDER/actual-cookiecutterassert-output.txt $FOLDER/expected-cookiecutterassert-output.txt
  if [ $? != 0 ] ; then
    echo "INTEGRATION TEST FAILED DUE TO INCORRECT COMMAND OUTPUT"
    exit 1
  fi
}


execute_test 0 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/basicIntegrationTest
execute_test 1 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/failingIntegrationTest
execute_test 0 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/runScriptSucceeds
execute_test 0 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/fileContainsLine
execute_test 0 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/templateHasTestFolder
execute_test 0 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/regexRuleTest
execute_test 0 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/fileContainsSnippet
execute_test 0 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/inheritedConfig
execute_test 0 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/onlyInheritedConfig
execute_test 1 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/binaryFileDiff
execute_test 1 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/no-test-warning
execute_test 1 pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/no-test-cases-warning
execute_test_expected_output 1 ./integrationTests/visible-spaces pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/visible-spaces
execute_test_expected_output 1 ./integrationTests/visible-tabs pipenv run python runIntegrationTest.py --templatefolder ./integrationTests/visible-tabs
echo "All Integration Tests PASSED!!!!!"