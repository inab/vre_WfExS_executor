cwl_static_keys = ["cwl_wf_url", "CWL workflow", "hidden"]


def __init__(self, _id, cwl_wf_url):
    """

    """
    self.cwl_wf = cwl_wf_url
    if self.cwl_wf is not None:
        self.fetch_and_validate_cwl()  # fetch and validate CWL workflow

    # set arguments
    self.arguments = self.set_arguments(_id)


def get_arguments(self):
    """
    Get arguments
    """
    return self.arguments


def set_arguments(self, _id):
    """
    Set arguments
    """
    args = list()
    cwl_wf_url = {
        "name": self.cwl_static_keys[0],
        "description": self.cwl_static_keys[1],
        "help": self.cwl_static_keys[1] + " for " + _id,
        "type": self.cwl_static_keys[2],
        "value": self.cwl_wf,
        "required": True
    }
    args.append(cwl_wf_url)  # add arguments
    self.arguments = args  # save arguments

    return self.arguments