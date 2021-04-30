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

import yaml
import os

from wfexs_backend.workflow import WF
from yaml import Loader as YAMLLoader

local_config = {}
with open("tests/local_config.yaml", mode="r", encoding="utf-8") as cf:
    local_config = yaml.load(cf, Loader=YAMLLoader)

workflow_meta = {}
with open("tests/cosifer_test1_cwl.yaml", mode="r", encoding="utf-8") as wcf:
    workflow_meta = yaml.load(wcf, Loader=YAMLLoader)

wfInstance = WF(local_config, "tests")
wfInstance.fromForm(workflow_meta)
print(wfInstance)
wfInstance.fetchWorkflow()
localWF = os.path.join(wfInstance.localWorkflow.dir, wfInstance.localWorkflow.relPath)
print(localWF)
wfInstance.setupEngine()
wfInstance.materializeWorkflow()
# with open(localWF, "r") as wf:
#     wf = yaml.safe_load(wf)
#     print(wf)
#     inputs = wf['inputs']
#     outputs = wf['outputs']
#     print(inputs)
# print(outputs)

# fetchWorkflow()
# materializeInputs()
# CONTAINERS
