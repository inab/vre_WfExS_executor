#!/usr/bin/env python

"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import absolute_import

import json

from cwltool.load_tool import fetch_document
from cwltool.load_tool import resolve_and_validate_document
from cwltool.load_tool import make_tool
from cwltool.workflow import default_make_tool


class CWL:
    """
    CWL workflow class
    """

    def __init__(self, cwl_wf_url):
        """
        Init function
        """
        self.cwl_wf = cwl_wf_url

    def fetch_and_validate_cwl(self):
        """
        Fetch and Validate CWL workflow
        """
        try:
            # fetch CWL workflow
            loadingContext, workflowobj, uri = fetch_document(self.cwl_wf)
            loadingContext.do_update = False

            # validate CWL workflow
            loadingContext, uri = resolve_and_validate_document(loadingContext, workflowobj, uri)
            processobj = loadingContext.loader.resolve_ref(uri)[0]
            return loadingContext, uri, processobj

        except Exception as error:
            errstr = "Unable to fetch and validate the CWL workflow {}. ERROR: {}".format(self.cwl_wf, error)
            raise Exception(errstr)

    def extract_data_from_cwl(self):
        """
        Get inputs, outputs and list of tools from CWL workflow.

        :return: inputs, outputs and CWL workflow tools dependencies
        :rtype: list, list, list
        """
        tools_list = list()
        try:
            # fetch and validate CWL workflow
            loadingContext, uri, processobj = self.fetch_and_validate_cwl()
            cwl_document = make_tool(uri, loadingContext)

            # get inputs and outputs
            inputs_list = json.dumps(cwl_document.inputs_record_schema["fields"], indent=4)
            outputs_list = json.dumps(cwl_document.outputs_record_schema["fields"], indent=4)

            # get tools dependencies
            for item in cwl_document.metadata["steps"]:
                [tools_list.append(item[key]) for key in item.keys() if key == "run"]

            return inputs_list, outputs_list, tools_list

        except Exception as error:
            errstr = "Unable to extract inputs, outputs and the tools dependencies from CWL workflow {}. ERROR: {}".format(
                self.cwl_wf, error)
            raise Exception(errstr)


if __name__ == '__main__':
    url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example.cwl"
    cwl_wf = CWL(url)

    # extract data from CWL
    inputs, outputs, tools = cwl_wf.extract_data_from_cwl()
    print("INPUTS:\n{0}\n OUTPUTS:\n{1}\n TOOLS:\n{2}".format(inputs, outputs, json.dumps(tools, indent=2)))
