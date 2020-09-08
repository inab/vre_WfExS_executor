import json
import pathlib
import zipfile
import os

from rocrate import rocrate


from lib.read_cwl import read_config_from_cwl_file


def unzip(rocrate_zip_path):
    """
    Unzip RO-Crate ZIP file specified by rocrate_path

    :param rocrate_zip_path: RO-Crate ZIP file
    :type rocrate_zip_path: str
    """
    try:
        with zipfile.ZipFile(rocrate_zip_path, 'r') as zpf:
            zpf.extractall(os.path.dirname(rocrate_zip_path) + "/ro/")

    except Exception:
        raise AssertionError("Cannot unzip the provided RO-Crate ZIP file: {}".format(rocrate_zip_path))


def get_cwl_wf_url(rocrate_path):
    """
    Get CWL URL of RO-Crate

    :param rocrate_path: RO-Crate file
    :type rocrate_path: str
    """
    try:
        ro_crate = rocrate.ROCrate(rocrate_path, load_preview=True)
        return ro_crate.root_dataset['isBasedOn']

    except Exception:
        raise AssertionError("Cannot return the provided CWL URL from: {}".format(rocrate_path))


if __name__ == '__main__':
    # TODO download RO-Crate from Workflow Hub

    abs_path = str(pathlib.Path().absolute())

    # unzip RO-Crate
    rocrate_zip_path = abs_path + "/workflow-119-1.crate.zip"
    unzip(rocrate_zip_path)

    # get CWL URL of RO-Crate
    rocrate_path = abs_path + "/ro/"
    cwl_wf_url = get_cwl_wf_url(rocrate_path)
    print(cwl_wf_url)

    # TODO validate cwl_wf_url

    cwl_wf_url_parsed = cwl_wf_url.replace("https://github.com", "https://raw.githubusercontent.com").replace(
        cwl_wf_url.split("/")[5] + "/", "")

    print(cwl_wf_url_parsed)

    config, metadata = read_config_from_cwl_file(cwl_wf_url_parsed)
    with open('config.json', 'w') as fp:
        fp.write(json.dumps(config, indent=2))

    with open('metadata.json', 'w') as fp:
        fp.write(json.dumps(metadata, indent=2))
