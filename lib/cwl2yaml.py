import os
import sys
import urllib.request

import yaml

# cwl input
remote_cwl = 'https://raw.githubusercontent.com/inab/ipc_workflows/main/cosifer/cwl/cosifer.cwl'

# read cwl file and load it as yaml
yaml_obj_remote = urllib.request.urlopen(remote_cwl)
yaml_obj_remote = yaml.safe_load(yaml_obj_remote)

# check cwlVersion
if 'cwlVersion' not in list(yaml_obj_remote.keys()):
    print('ERROR: could not get the cwlVersion')
    sys.exit(1)

# import parsed based on cwlVersion
if yaml_obj_remote['cwlVersion'] == 'v1.0':
    from cwl_utils import parser_v1_0 as parser
elif yaml_obj_remote['cwlVersion'] == 'v1.1':
    from cwl_utils import parser_v1_1 as parser
elif yaml_obj_remote['cwlVersion'] == 'v1.2':
    from cwl_utils import parser_v1_2 as parser
else:
    print('ERROR: Version error. Did not recognise {} as a CWL version'.format(yaml_obj_remote['cwlVersion']))
    sys.exit(1)

# import cwl object
cwl_obj = parser.load_document(yaml_obj_remote)

cwl_inputs_dict = {}
cwl_outputs_dict = {}
for inp in cwl_obj.inputs:
    # print(inp.id)
    input_id = os.path.basename(inp.id)
    if isinstance(inp.type, list):  # optional params
        input_type = inp.type[1]
    else:
        input_type = inp.type

    if input_type == "File":
        cwl_inputs_dict[input_id] = {'c-l-a-s-s': input_type, 'url': ''}

    else:
        cwl_inputs_dict[input_id] = {'c-l-a-s-s': input_type}

for out in cwl_obj.outputs:
    output_id = os.path.basename(out.id)
    output_type = out.type
    if output_type == 'File':
        cwl_outputs_dict[output_id] = {'c-l-a-s-s': output_type, 'preferredName': ''}

    else:
        cwl_outputs_dict[output_id] = {'c-l-a-s-s': output_type}

# create dict
cwl_dict = {
    'workflow_id': remote_cwl,
    'workflow_config': {'secure': False},  # bottom secure
    'params': cwl_inputs_dict,
    'outputs': cwl_outputs_dict

}
# create yaml file from cwl_dict
with open('../tests/cosifer_test3_cwl.yaml', mode='w', encoding='utf-8') as yaml_input:
    yaml.dump(cwl_dict, yaml_input, Dumper=yaml.Dumper)
