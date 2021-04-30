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
