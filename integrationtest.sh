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
  if [ $? != $EXPECTED_RESULT ] ; then
    echo "INTEGRATION TEST FAILED!!!"
    exit 1
  fi
}

execute_test 0 python runIntegrationTest.py --templatefolder ./integrationTests/basicIntegrationTest
execute_test 1 python runIntegrationTest.py --templatefolder ./integrationTests/failingIntegrationTest
execute_test 0 python runIntegrationTest.py --templatefolder ./integrationTests/runScriptSucceeds
execute_test 0 python runIntegrationTest.py --templatefolder ./integrationTests/fileContainsLine
execute_test 0 python runIntegrationTest.py --templatefolder ./integrationTests/templateHasTestFolder
execute_test 0 python runIntegrationTest.py --templatefolder ./integrationTests/regexRuleTest
execute_test 0 python runIntegrationTest.py --templatefolder ./integrationTests/fileContainsSnippet
execute_test 0 python runIntegrationTest.py --templatefolder ./integrationTests/inheritedConfig
execute_test 0 python runIntegrationTest.py --templatefolder ./integrationTests/onlyInheritedConfig
execute_test 1 python runIntegrationTest.py --templatefolder ./integrationTests/binaryFileDiff
execute_test 1 python runIntegrationTest.py --templatefolder ./integrationTests/no-test-warning
execute_test 1 python runIntegrationTest.py --templatefolder ./integrationTests/no-test-cases-warning

echo "All Integration Tests PASSED!!!!!"