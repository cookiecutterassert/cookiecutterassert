set PYTHON_CMD=python
!command -v python3 && set PYTHON_CMD=python3
echo %PYTHON_CMD%
%PYTHON_CMD% --version
%PYTHON_CMD% -m venv venv
venv\Scripts\activate.bat