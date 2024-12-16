from medoc_api.enums import DEVICE_TAG, COMMAND_ID


MAX_LENGTH = 512


class message:
    def __init__(self):
        self.command_id = COMMAND_ID.Undefined
        self.command_array = None
        self.command_token = None
        self.command_tag = DEVICE_TAG.Master

    def __str__(self):
        command = str(self.command_id)
        tag = str(self.command_tag)

        return f"COMMAND: {command} TOKEN: {self.command_token} TAG: {tag}"
