#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2020-2021 Barcelona Supercomputing Center (BSC), Spain
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools
import re
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = list()
    egg = re.compile(r"#[^#]*egg=([^=&]+)")
    for line in f.read().splitlines():
        m = egg.search(line)
        requirements.append(line if m is None else m.group(1))

setuptools.setup(
    name='generic_wrapper',
    version='generic_wrapper_backend_version',
    author='Laura Rodriguez-Navas',
    author_email='lrodrin@users.noreply.github.com',
    license=license,
    description='Generic Wrapper backend',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/inab/generic_wrapper',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
