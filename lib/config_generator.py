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

from json import dumps

from dataclasses_serialization.json import JSONSerializer

from schema_generator import *

# example
keywords = ["whatever"]
inputs = [{'id': 'data_matrix', 'type': 'File'}, {'id': 'gmt_filepath', 'type': 'File?'},
          {'id': 'index_col', 'type': 'int?'}, {'id': 'outdir', 'type': 'string'},
          {'id': 'separator', 'type': 'string?'}]

owner = setOwner("My Name", "My Institution", "myEmail@intitution.cat", "https://MyInstitution.institution.cat/MyGroup")
cloud = setCloud("PMES", "COMPSs", 1, 1, True)
infrastructure = setInfrastructure(12, 4, "/VM/path/where/main/executable/is/going/to/be/MyTool.py", cloud)
input_files, arguments = setInputs(inputs)
tool = setTool(owner, keywords, infrastructure, input_files, arguments)
print(dumps(JSONSerializer.serialize(tool), indent=2))
