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
import os

from lib.cwl import CWL


class Form:
    """

    """

    def __init__(self, id, elem):
        """

        """
        self._id = id
        self._type = os.path.basename(elem).split(".")[1]  # get type of elem
        self.configuration = dict()
        self.arguments = list()

        if self._type == "cwl":  # CWL workflow
            cwl = CWL(self._id, elem)
            self.arguments = cwl.get_arguments()
            self.configuration.update({"arguments": self.arguments})  # TODO constant key

            # TODO validate configuration


if __name__ == '__main__':
    _id = "cwl_samtools_split"
    cwl_wf = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example.cwl"
    spec = Form(_id, cwl_wf)
    print(json.dumps(spec.configuration, indent=2))
