import logging
import json
import os

logger = logging.getLogger(__name__)


class input_commands():
    """

    """
    def __init__(self):
        self.commands = []

    def load_commands(self, path):
        """
        :param path: os path to commands preferences file
        :return:
        """
        if not os.path.isfile(path):
            raise Exception("invalid command file path {!r}".format(path))
        logger.info("reading commands from file %s...", path)
        with open(path) as json_file:
            data = json.load(json_file)
            for item in data['Commands']:
                self.commands.append(item)

        logger.info("total commands read from file %s ::: is %d", path, len(data['Commands']))