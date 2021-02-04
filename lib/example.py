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
