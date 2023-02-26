import datetime
import logging
import os


def set_up_logger():
    if not os.path.exists('./Logs'):
        os.makedirs('./Logs')
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        filename="./Logs/" + str(datetime.datetime.now()), filemode='w', level='DEBUG')
    logger = logging.getLogger(__name__)
    logger.info("Initiating Logger")
    return logger
