
''''This file contains classes and functions used to start the playing sessions'''

import os
import logging
import sys

# from ..fundamentals import config
# from ..fundamentals import open_vba

#
# def initialize_logger(console_level=logging.DEBUG):
#
#     logging_directory = os.path.dirname(os.path.realpath(__file__)) + '\\log'
#
#     format_str = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
#     logging.basicConfig(
#                         # filename=logging_directory,
#                         # stream=sys.stdout,
#                         level=console_level,
#                         format=format_str,
#     )
#     # # set up logging to console
#     # stream_handler = logging.StreamHandler()
#     # stream_handler.setLevel(console_level)
#     # # set a format which is simpler for console use
#     # formatter = logging.Formatter(format_str)
#     # stream_handler.setFormatter(formatter)
#     # # add the handler to the root logger
#     # logging.getLogger('').addHandler(stream_handler)

#
def get_custom_logger(console_level='DEBUG'):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logging_directory = os.path.dirname(os.path.realpath(__file__)) + '\\log'

    # logging.basicConfig(filename=logging_directory, stream=sys.stdout, level=logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    if console_level == 'INFO':
        handler.setLevel(logging.INFO)
    elif console_level == 'DEBUG':
        handler.setLevel(logging.DEBUG)
    elif console_level == 'WARNING':
        handler.setLevel(logging.WARNING)
    elif console_level == 'ERROR':
        handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(logging_directory, "all.log"), "w")
    handler.setLevel(logging.DEBUG)  # log everything
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
#
#     return logger


def start_bot(console_level='INFO'):
    open_vba()
    # initialize_logger(logging_directory='log', console_level=console_level, include_lowest_level=False)
    # logger.debug('Loading templates')
    #load_templates()
    # if console_level == 'DEBUG':
    #     #from debug.debug_location import open_debug_screen
    #     open_debug_screen()

    # more stuff here regarding the the console_level


if __name__ == '__main__':
    initialize_logger(console_level=logging.DEBUG)
    logger = logging.getLogger()
    logger.info('Loading templates')
