
### MacOS / Linux First Time Setup
Create a new python virtual environment for this repo:

```./createVEnv.sh```

This will also install all requirements.
Then go to [Run a local version](#run-a-local-version)

### Windows First Time Setup

```createVEnv.bat```

then, in the windows venv shell

```installRequirements.bat```

Then go to [Run a local version](#run-a-local-version)
# Every time you open a terminal
### MacOS / Linux
Activate the virtual environment:

```source venv/bin/activate``` 

### Windows
Activate the virtual environment:

```venv\Scripts\activate.bat```

# Whenever you update dependencies
### MacOS / Linux
Install dependencies:

```./installRequirements.sh```

### Windows
Install dependencies:

```installRequirements.bat```

# Whenever you install a new Python Library to your virtual environment
### MacOS / Linux
Save Library dependencies:

```./saveRequirements.sh```

### Windows
Save Library dependencies:

```saveRequirements.bat```

# Run tests
## Execute all tests:
```./test.sh``` or ```pytest```


## Execute unit tests:
```./unittest.sh```


## Execute integration tests:
```./integrationtest.sh```

