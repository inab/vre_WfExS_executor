from sys import platform

import yaml
import platform

from yaml import Loader as YAMLLoader
from wfexs_backend.workflow import WF

local_config = {}
workflow_config = {}
with open("tests/local_config.yaml", mode="r", encoding="utf-8") as cf:
    local_config = yaml.load(cf, Loader=YAMLLoader)
with open("tests/cosifer_test1_cwl.yaml", mode="r", encoding="utf-8") as cf:
    workflow_config = yaml.load(cf, Loader=YAMLLoader)
print(local_config)
print(workflow_config)

wfInstance = WF.fromForm(workflow_meta=workflow_config, local_config=local_config)
print(wfInstance)
# wfInstance.fetchWorkflow()
# localWF = os.path.join(wfInstance.localWorkflow.dir, wfInstance.localWorkflow.relPath)
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
