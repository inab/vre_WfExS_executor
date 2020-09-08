import json
import os
import sys
from ruamel.yaml.comments import CommentedMap, CommentedSeq


def remove_non_printable_characters(string_to_clean):
    return "".join(c for c in string_to_clean if c.isprintable())


def clean_string(string_to_clean):
    # removes leading and tailing whitespaces
    # and converts unicode strings to ascii:
    print_pref = "[clean_string]:"
    if isinstance(string_to_clean, str):
        str_cleaned = remove_non_printable_characters(string_to_clean).strip()
    elif isinstance(string_to_clean, int):
        str_cleaned = str(string_to_clean)
    elif isinstance(string_to_clean, float):
        str_cleaned = str(string_to_clean)
    elif isinstance(string_to_clean, bool):
        str_cleaned = str(string_to_clean)
    else:
        raise AssertionError(print_pref + "E: is not a string or number")
    return str_cleaned


def is_basic_type_instance(value):
    return (isinstance(value, int) or
            isinstance(value, float) or
            isinstance(value, str) or
            isinstance(value, bool))


def read_inp_rec_type_field(inp_rec_type):
    print_pref = "[read_inp_type]:"
    is_array = False
    null_allowed = False
    null_items_allowed = False
    allowed_selection = [""]

    # if optional:
    if isinstance(inp_rec_type, list):
        if len(inp_rec_type) == 2 and "null" in inp_rec_type:
            null_allowed = True
            inp_rec_type.remove("null")
            inp_rec_type = inp_rec_type[0]
        else:
            raise AssertionError(print_pref + "unkown type" +
                                 ": lists of type are only supported when one of two elements is \"null\"")
    # array or type enum:
    if isinstance(inp_rec_type, dict):
        assert "type" in inp_rec_type.keys(), print_pref + " unkown type"

        # if array:
        if "items" in inp_rec_type.keys():
            if inp_rec_type["type"] == "array":
                is_array = True
                inp_rec_type = inp_rec_type["items"]
                if isinstance(inp_rec_type, dict):
                    if "type" in inp_rec_type.keys() and inp_rec_type["type"] == "array":
                        raise AssertionError(print_pref + " arrays of arrays are not supported.")
                    else:
                        raise AssertionError(print_pref + " unkown type")
            else:
                raise AssertionError(print_pref + " unkown type")

            # if "null" is allowed as array item:
            if isinstance(inp_rec_type, list):
                if len(inp_rec_type) == 2 and "null" in inp_rec_type:
                    null_items_allowed = True
                    inp_rec_type.remove("null")
                    inp_rec_type = inp_rec_type[0]
                else:
                    raise AssertionError(print_pref + " unkown type" +
                                         ": lists of type are only supported when one of two elements is \"null\"")
        # if type enum
        elif inp_rec_type["type"] == "enum":
            allowed_selection = inp_rec_type["symbols"]
            inp_rec_type = "string"
        else:
            raise AssertionError(print_pref + " unkown type")

    if isinstance(inp_rec_type, str):
        type_ = inp_rec_type
    else:
        raise AssertionError(print_pref + " unkown type")

    return type_, null_allowed, is_array, null_items_allowed, allowed_selection


def read_config_from_cwl_file(cwl_file):
    print_pref = "[read_cwl_file]:"
    configs = {}
    metadata = {
        "doc": "",
        "workflow_name": os.path.basename(cwl_file),
        "workflow_path": os.path.abspath(cwl_file),
        "workflow_type": "CWL"
    }
    # cwltool needs to be imported on demand since
    # repeatedly calling functions on a document named
    # with same name caused errors.
    from cwltool.context import LoadingContext
    from cwltool.load_tool import load_tool
    from cwltool.workflow import default_make_tool
    loadingContext = LoadingContext({"construct_tool_object": default_make_tool, "disable_js_validation": True})

    try:
        cwl_document = load_tool(cwl_file, loadingContext)
    except AssertionError as e:
        raise AssertionError(print_pref + "failed to read cwl file \"" + cwl_file + "\": does not exist or is invalid")

    # inputs
    inp_records = cwl_document.inputs_record_schema["fields"]
    print(json.dumps(inp_records, indent=2))

    # outputs
    out_records = cwl_document.outputs_record_schema["fields"]

    # workflow dependencies
    tools_list = list()
    for item in cwl_document.metadata["steps"]:
        [tools_list.append(item[key]) for key in item.keys() if key == "run"]

    if "doc" in cwl_document.tool:
        metadata["doc"] = cwl_document.tool["doc"]

    for inp_rec in inp_records:
        name = clean_string(inp_rec["name"])
        # read type:
        try:
            type_, null_allowed, is_array, null_items_allowed, allowed_selection = read_inp_rec_type_field(
                inp_rec["type"])
        except Exception as e:
            raise AssertionError(print_pref + "E: reading type of param \"{}\": {}".format(name, str(e)))

        # get the default:
        if "default" in inp_rec:
            if is_basic_type_instance(inp_rec["default"]):
                default_value = [clean_string(inp_rec["default"])]
            else:
                if is_array and isinstance(inp_rec["default"], list):
                    default_value = []
                    for entry in inp_rec["default"]:
                        if is_basic_type_instance(inp_rec["default"]):
                            default_value.append(clean_string(entry))
                        else:
                            print(print_pref + "W: invalid default value for parameter " + name +
                                  ": will be ignored", file=sys.stderr)
                            default_value = [""]

                elif type_ == "File" and isinstance(inp_rec["default"], dict):
                    print(print_pref + "W: invalid default value for parameter " + name +
                          ": defaults for File class are not supported yet; will be ignored", file=sys.stderr)
                    default_value = [""]

                else:
                    print(print_pref + "W: invalid default value for parameter " + name +
                          ": will be ignored", file=sys.stderr)
                    default_value = [""]
        else:
            default_value = [""]

        # read secondary files:
        if type_ == "File" and "secondaryFiles" in inp_rec:
            if isinstance(inp_rec["secondaryFiles"], str):
                secondary_files = [inp_rec["secondaryFiles"]]
            elif isinstance(inp_rec["secondaryFiles"], CommentedMap) and \
                    "pattern" in inp_rec["secondaryFiles"].keys():
                secondary_files = [inp_rec["secondaryFiles"]["pattern"]]
            elif isinstance(inp_rec["secondaryFiles"], CommentedSeq) or isinstance(inp_rec["secondaryFiles"], list):
                secondary_files = []
                for sec_file in inp_rec["secondaryFiles"]:
                    if isinstance(sec_file, CommentedMap) and "pattern" in sec_file:
                        secondary_files.append(sec_file["pattern"])
                    elif isinstance(sec_file, str):
                        secondary_files.append(sec_file)
                    else:
                        raise AssertionError(print_pref + "E: invalid secondaryFiles field for parameter " + name)
            else:
                raise AssertionError(print_pref + "E: invalid secondaryFiles field for parameter " + name)
        else:
            secondary_files = [""]

        # read doc:
        if "doc" in inp_rec:
            doc = inp_rec["doc"]
        else:
            doc = ""

        # assemble config parameters:
        inp_configs = {
            "type": type_,  # el que fa triar input file o argument
            "is_array": is_array,  # si array allow_multiple == True, else otherwise
            "null_allowed": null_allowed,  # si es False required sera True, else otherwise
            "null_items_allowed": null_items_allowed,
            "secondary_files": secondary_files,
            "default_value": default_value,  # TODO per aqui podriem recollir els strings estranys like @RG de CHOP
            "allowed_selection": allowed_selection,  # TODO per aqui podriem controlar
            "doc": doc
        }

        # add to configs dict:
        configs[name] = inp_configs

    defineIO(configs)  # TODO create input files, output files and arguments

    return configs, metadata


def defineIO(inputs):
    input_files = {}
    arguments = {}

    for in_rec in inputs:
        name = in_rec
        input = inputs[name]

        if input['type'] == "File":

            # assemble input files parameters:
            inp_files = {
                "name": name,
                "description": input['doc'],
                "help": input['doc'],
                # "file_type": ???
                # "data_type": ???
                "required": input['null_items_allowed'],
                "allow_multiple": input['is_array']
            }

            # add to input_files dict:
            input_files[name] = inp_files

        else:

            # assemble input files parameters:
            inp_arguments = {
                "name": name,
                "description": input['doc'],
                "help": input['doc'],
                "type": input['type'],
                "default": input['default_value']
            }

            # add to arguments dict:
            arguments[name] = inp_arguments

    print(input_files)
    print(arguments)

    d = {
        "input_files": [input_files],
        "arguments": [arguments]

    }
    with open('defineIO.json', 'w') as fp:
        fp.write(json.dumps(d, indent=2))


wf_basic = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example.cwl"
# wf_transDecoder = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/trans_decoder/data/workflows/TransDecoder-v5-wf-2steps.cwl"
wf_kfdrc = "https://raw.githubusercontent.com/kids-first/kf-alignment-workflow/dm-ipc-fixes/workflows/kfdrc_alignment_wf_cyoa.cwl"
wf_wetlab2variations = "https://raw.githubusercontent.com/inab/Wetlab2Variations/eosc-life/cwl-workflows/workflows/workflow.cwl"

config, metadata = read_config_from_cwl_file(wf_wetlab2variations)
with open('config.json', 'w') as fp:
    fp.write(json.dumps(config, indent=2))

with open('metadata.json', 'w') as fp:
    fp.write(json.dumps(metadata, indent=2))
