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

import setuptools
import os.path
import os
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

version = os.getenv("TAG_NAME")
if (version.startswith("v")):
    version = version[1:]

print("Creating package for version {}".format(version))

with open("README.md", "r") as fh:
    long_description = fh.read()

pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)

setuptools.setup(
    name="cookiecutterassert",
    version=version,
    author="Micah Tessler",
    author_email="mtessler@ford.com",
    description="Automated testing framework for python cookie cutter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cookiecutterassert/cookiecutterassert",
    packages=setuptools.find_packages(exclude=['test', 'test.*', '*.test.*', 'test.rules']),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ],
    python_requires='>=3.8',
    license='Apache Software License',
    license_file='LICENSE.txt',
    entry_points = {
        'console_scripts': ['cookiecutterassert=cookiecutterassert.main:runAllTests'],
    }
)
