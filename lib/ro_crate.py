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
import re
from urllib import request

import requests
import ssl

# change only for OSX
# TODO if os.system is darwin
ssl._create_default_https_context = ssl._create_unverified_context


ro_path = "/Users/laurarodrigueznavas/BSC/generic_wrapper/tests/ro_crate/data/ro-crate-metadata.jsonld"
# schema_path = "/Users/laurarodrigueznavas/BSC/generic_wrapper/tests/ro_crate/data/schema.jsonld"

ro_crate = json.loads(open(ro_path, encoding="utf-8").read())
# schema = json.loads(open(schema_path, encoding="utf-8").read())
# schema_map = dict((e["@id"], e) for e in schema["@graph"])


class ROCrate:
    """
    RO-Crate class
    """

    def __init__(self, identifier):
        """
        Init function
        """
        self.id = identifier

    def find_entity(self):
        """

        """
        for item in ro_crate["@graph"]:
            if item.get("@id", None) == self.id:
                return item  # CWL workflow

    def get_url(self):
        """

        """
        _url = self.find_entity()["url"]
        return _url

    def get_items(self):
        """

        """
        items = self.find_entity()["hasPart"]
        return items


def validate_url(url_wf):
    try:
        _ = request.urlopen(url_wf)

    except Exception:
        raise AssertionError("Cannot open the provided URL: {}".format(url_wf))


if __name__ == '__main__':
    ro = ROCrate("./")

    # get URL
    url = ro.get_url()
    print(url)

    validate_url(url)

    # get elements to download
    items = ro.get_items()
    print(items)

    rule = re.search(r"\b(workflows/)\b", url)  # search position of workflows folder
    index = rule.start()

    # divide url in two parts
    abs_path = url[:index]
    sub_path = url[index:]

    files = list()
    for elem in items: # for each item to download
        # if "workflows" in elem["@id"] or "tools" in elem["@id"]:
        path = abs_path + elem["@id"]
        user = path.split("/")[3]
        project = path.split("/")[4]

        url_raw = 'https://api.github.com/repos/{}/{}/contents/{}'.format(user, project, elem["@id"])
        req = requests.get(url_raw)
        if req.status_code == requests.codes.ok:
            req = req.json()
            files.append(req["download_url"])
        # else:
        #     print('Content was not found.')

    print(json.dumps(files, indent=2))


