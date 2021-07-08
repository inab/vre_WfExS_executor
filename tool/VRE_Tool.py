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
import json
import os
import subprocess
import time

from basic_modules.tool import Tool
from utils import logger


class WfExS(Tool):
    """
    This class define WfExS Tool.
    """
    DEFAULT_KEYS = ['execution', 'project', 'description']  # config.json default keys
    PYTHON_SCRIPT_PATH = "/wfexs/WfExS-backend.py"

    def __init__(self, configuration=None):
        """
        Init function

        :param configuration: a dictionary containing parameters that define how the operation should be carried out,
        which are specific to WfExS tool.
        :type configuration: dict
        """
        Tool.__init__(self)

        if configuration is None:
            configuration = {}

        self.configuration.update(configuration)

        for k, v in self.configuration.items():
            if isinstance(v, list):
                self.configuration[k] = ' '.join(v)

        # Init variables
        self.current_dir = os.path.abspath(os.path.dirname(__file__))
        self.parent_dir = os.path.abspath(self.current_dir + "/../")
        self.execution_path = self.configuration.get('execution', '.')
        if not os.path.isabs(self.execution_path):  # convert to abspath if is relpath
            self.execution_path = os.path.normpath(os.path.join(self.parent_dir, self.execution_path))

        self.arguments = dict(
            [(key, value) for key, value in self.configuration.items() if key not in self.DEFAULT_KEYS]
        )

        # Init specific variables
        self.execution_provenance = {}

    def run(self, input_files, input_metadata, output_files, output_metadata):
        """
        The main function to run the WfExS tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        :param input_metadata: Dictionary of files metadata.
        :type input_metadata: dict
        :param output_files: Dictionary of the output files locations. Expected to be generated.
        :type output_files: dict
        :param output_metadata: # TODO
        :type output_metadata: list
        :return: # TODO
        :rtype: dict, dict
        """
        try:
            # Set and validate execution directory. If not exists the directory will be created.
            os.makedirs(self.execution_path, exist_ok=True)

            # Set and validate execution parent directory. If not exists the directory will be created.
            execution_parent_dir = os.path.dirname(self.execution_path)
            os.makedirs(execution_parent_dir, exist_ok=True)

            # Update working directory to execution path
            os.chdir(self.execution_path)

            # Tool Execution
            self.toolExecution(input_files)

            if len(self.execution_provenance) != 0:
                # Create and validate the output files from Tool execution
                # TODO

                return output_files, output_metadata

            # else: TODO error handling

        except:
            errstr = "VRE WfExS tool execution failed. See logs."
            logger.fatal(errstr)
            raise Exception(errstr)

    def toolExecution(self, input_files):
        """
        The main function to run the WfExS tool.

        :param input_files: Dictionary of input files locations.
        :type input_files: dict
        """
        output = None
        error = None
        rc = None
        try:
            # Get workflow_config_filename and local_config_filename
            workflow_config = input_files.get("workflow_config_filename")
            local_config = input_files.get("local_config_filename")
            if not os.path.isabs(workflow_config):
                workflow_config = os.path.normpath(os.path.join(self.parent_dir, workflow_config))
            if not os.path.isabs(local_config):
                local_config = os.path.normpath(os.path.join(self.parent_dir, local_config))

            # Get command
            wfexs_cmd = self.arguments.get("command")
            if wfexs_cmd is None:
                errstr = "command argument must be defined."
                logger.fatal(errstr)
                raise Exception(errstr)

            # WfExS execution
            if os.path.isfile(workflow_config) and os.path.isfile(local_config):

                cmd = [
                    'python',
                    self.PYTHON_SCRIPT_PATH,
                    '-d',
                    '-L',
                    local_config,
                    '-W',
                    workflow_config,
                    wfexs_cmd
                ]

                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Sending the stdout to the log file
                for line in iter(process.stderr.readline, b''):
                    print(line.rstrip().decode("utf-8").replace("", " "))

                rc = process.poll()
                while rc is None:
                    rc = process.poll()
                    time.sleep(0.1)

                if rc is not None and rc != 0:
                    logger.progress("Something went wrong inside the WfExS execution. See logs.", status="WARNING")
                else:
                    logger.progress("WfExS execution finished successfully", status="FINISHED")

                # Save processed outputs from WfExS execution
                output, error = process.communicate()
                self.execution_provenance = json.loads(output)

            else:
                errstr = "workflow and local configurations input files must be defined."
                logger.fatal(errstr)
                raise Exception(errstr)

        except:
            errstr = "WfExS execution failed. See logs."
            logger.error(errstr)
            if rc is not None:
                logger.error("RETVAL: {}".format(rc))
            if output is not None:
                logger.error("STDOUT: " + output.decode("utf-8", errors="ignore"))
            if error is not None:
                logger.error("STDERR: " + error.decode("utf-8", errors="ignore"))
            raise Exception(errstr)
