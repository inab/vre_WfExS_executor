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
import argparse
import logging
import sys

import yaml
import os

from yaml import Loader as YAMLLoader

from wfexs_backend.workflow import WF

if __name__ == '__main__':

    # Basic main for minimal execution
    ap = argparse.ArgumentParser(description="WfExS (workflow execution service) backend")
    ap.add_argument('-d', '--debug', dest='logLevel', action='store_const', const=logging.DEBUG,
                    help='Show debug messages (use with care, as it can disclose passphrases and passwords)')
    ap.add_argument('-L', '--local-config', dest="localConfigFilename", help="Local installation configuration file")
    ap.add_argument('-W', '--workflow-config', dest="workflowConfigFilename",
                    help="Configuration file, describing workflow and inputs")
    ap.add_argument('command', help='Command to run', nargs='?', default='execute')

    args = ap.parse_args()

    # Setting up the log
    loggingConf = {
        'format': '%(asctime)-15s - [%(levelname)s] %(message)s',
    }

    if args.logLevel:
        loggingConf['level'] = args.logLevel

    logging.basicConfig(**loggingConf)

    # First, try loading the configuration file
    localConfigFilename = args.localConfigFilename
    if localConfigFilename and os.path.exists(localConfigFilename):
        with open(localConfigFilename, mode="r", encoding="utf-8") as cf:
            local_config = yaml.load(cf, Loader=YAMLLoader)
    else:
        local_config = {}
        if localConfigFilename and not os.path.exists(localConfigFilename):
            print("[WARNING] Configuration file {} does not exist".format(localConfigFilename), file=sys.stderr)

    # Second, try loading the workflow configuration file
    workflowConfigFilename = args.workflowConfigFilename
    if workflowConfigFilename and os.path.exists(workflowConfigFilename):
        with open(workflowConfigFilename, mode="r", encoding="utf-8") as wcf:
            workflow_meta = yaml.load(wcf, Loader=YAMLLoader)

    else:
        workflow_meta = {}
        if workflowConfigFilename and not os.path.exists(workflowConfigFilename):
            print("[WARNING] Workflow configuration file {} does not exist".format(workflowConfigFilename),
                  file=sys.stderr)

    wfInstance = WF(local_config, "tests")  # TODO hardcoded path for the Crypt4GH keys
    wfInstance.fromForm(workflow_meta)
    if args.command == 'execute':
        wfInstance.fetchWorkflow()
        wfInstance.setupEngine()
        wfInstance.materializeWorkflow()
        localWF = os.path.join(wfInstance.localWorkflow.dir, wfInstance.localWorkflow.relPath)
        localWFFile = open(localWF, "r")
        localWFYAML = yaml.safe_load(localWFFile)

        localWFInputs = localWFYAML['inputs']
        localWFOutputs = localWFYAML['outputs']
        print(localWFInputs)
        print(localWFOutputs)
