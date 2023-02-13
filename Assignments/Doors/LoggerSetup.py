import datetime
import logging

def set_up_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                        filename="./Logs/" + str(datetime.datetime.now()), filemode='w', level='DEBUG')
    logger = logging.getLogger(__name__)
    logger.info("Initiating Logger")
    return logger