export PYTHON_CMD=python
command -v python3 && export PYTHON_CMD=python3
echo $PYTHON_CMD
$PYTHON_CMD --version

$PYTHON_CMD -m venv venv
source ./venv/bin/activate
python --version
echo "Which Python:" $(which python)

source ./installRequirements.sh
