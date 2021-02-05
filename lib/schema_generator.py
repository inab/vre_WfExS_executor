from model import *


def setOwner(author, institution, contact, url):
    """

    :param author:
    :param institution:
    :param contact:
    :param url:
    :return:
    """
    return Owner(author, institution, contact, url)


def setCloud(launcher, workflow_type, minimum_v_ms, initial_v_ms, default_cloud):
    """

    :param launcher:
    :param workflow_type:
    :param minimum_v_ms:
    :param initial_v_ms:
    :param default_cloud:
    :return:
    """
    return Cloud(launcher, workflow_type, minimum_v_ms, initial_v_ms, default_cloud)


def setInfrastructure(memory, cpus, executable, cloud):
    """

    :param memory:
    :param cpus:
    :param executable:
    :param cloud:
    :return:
    """
    clouds = Clouds(cloud)
    return Infrastructure(memory, cpus, executable, clouds)


def is_required(param):
    """

    :param param:
    :return:
    """
    if "?" in param:
        return False
    else:
        return True


def is_multiple(param):
    """

    :param param:
    :return:
    """
    if "File" in param:
        return False
    else:
        return True


def setInputs(inputs):
    """

    :param inputs:
    :return:
    """
    wantedKeys = ["File", "'File[]'"]
    input_files, arguments = [], []
    for input in inputs:
        if input['type'].find("File") != -1:  # create new InputFile
            new_file = InputFile(
                name=input['id'],
                description="",  # TODO input['doc']
                help=None,
                file_type=[],
                data_type=[],
                required=is_required(input['type']),
                allow_multiple=is_multiple(input['type'])
            )
            input_files.append(new_file)

        else:  # create new Argument
            new_argument = Argument(
                name=input['id'],
                description="",  # TODO input['doc']
                help=None,
                type=input['type'],
                default=None
            )
            arguments.append(new_argument)

    return input_files, arguments


def setTool(owner, keywords, infrastructure, input_files, arguments):  # TODO
    """

    :param owner:
    :param keywords:
    :param infrastructure:
    :param input_files:
    :param arguments:
    :return:
    """
    return Tool(
        id="my_tool_id",
        name="My Tool",
        title="My Tool Complete Name",
        short_description="This is a one or two lines description of what 'My Tool' does.",
        long_description="This is a longer description of what 'My Tool' does. It includes information about the software use for it, the supported inputs, the expected results, etc.",
        url="https://github.com/.../MyTool",
        publication="http://dx.doi.org/xx.xxxx/xxxx/xxxxxx",
        owner=owner,
        keywords=keywords,
        keywords_tool=keywords,
        status=0,
        infrastructure=infrastructure,
        input_files=input_files,
        input_files_public_dir=[],
        input_files_combinations=[],
        arguments=arguments,
        has_custom_viewer=False,
        output_files=[]
    )
