## Designed to run local builds on a Mac to ensure you get the output you want
## output is published to the "build" folder
##
## To test different outputs, update the cookiecutter.json file
##
## To run this you need to first install pipx and the cookie cutter cli
## on Mac:
##
## brew install pipx
## pipx ensurepath
## pipx install cookiecutter

rm -rf build
mkdir build
cookiecutter --overwrite-if-exists --no-input --config-file testConfig.yaml --output-dir build .
cd build/MyApp
pwd
./createVEnv.sh
source venv/bin/activate
flask test
source venv/bin/deactivate
cd ../..
pwd
