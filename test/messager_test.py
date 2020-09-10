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

from unittest.mock import patch
from cookiecutterassert.messager import printError, printMessage, printSuccess
import click

message = "SomeMessage"
formattedMessage = "FormattedMessage"

@patch("click.echo")
def test_printMessageShouldUseClickEcho(echoMock):
    printMessage(message)
    
    echoMock.assert_called_once_with(message)

@patch("click.echo")
@patch("click.style")
def test_printErrorShouldPrintInRed(styleMock, echoMock):
    styleMock.return_value = formattedMessage

    printError(message)
    
    echoMock.assert_called_once_with(formattedMessage)
    styleMock.assert_called_once_with(message, fg="red")

@patch("click.echo")
@patch("click.style")
def test_printSuccessShouldPrintInGreen(styleMock, echoMock):
    styleMock.return_value = formattedMessage

    printSuccess(message)
    
    echoMock.assert_called_once_with(formattedMessage)
    styleMock.assert_called_once_with(message, fg="green")