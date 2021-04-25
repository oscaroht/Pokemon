
''''This file contains classes and functions used to start the playing sessions'''

import os
import time

import logging
#!/usr/bin/python
from fundamentals.config import config
from fundamentals.load_templates import load_templates
from fundamentals.open_vba import open_vba
from debug.debug_location import open_debug_screen

from io import StringIO

from glob import glob
import cv2



def initialize_logger(logging_directory='default', console_level='INFO', include_lowest_level=True):
    if logging_directory == 'default':
        param = config('../settings.ini', 'dirs')
        logging_directory = param['base_dir'] + param['log']
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

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

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(logging_directory, "error.log"), "a", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create warning file handler and set level to warning
    handler = logging.FileHandler(os.path.join(logging_directory, "warning.log"), "a", encoding=None, delay="true")
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create info file handler and set level to info
    handler = logging.FileHandler(os.path.join(logging_directory, "info.log"), "w", encoding=None, delay="true")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    if include_lowest_level:
        handler = logging.FileHandler(os.path.join(logging_directory, "all.log"), "w")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

def copy_to_db(conn, df, table):
    """
    Using copy to insert a dataframe to the database
    """

    cursor = conn.cursor()

    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False, sep='|')
    buffer.seek(0)

    try:
        #https://stackoverflow.com/questions/51522105/copy-dataframe-to-postgres-table-with-column-that-has-defalut-value
        cursor.copy_from(buffer, table, null='', sep='|')
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        cursor.close()
        raise
    cursor.close()







def start_bot(console_level='INFO'):
    open_vba()
    initialize_logger(logging_directory='log', console_level=console_level, include_lowest_level=False)
    #logger.debug('Loading templates')
    #load_templates()
    if console_level == 'DEBUG':
        open_debug_screen()

    # more stuff here regarding the the console_level

##### test
# img = load_templates()
# temp = Template('template_down_x1', 'Position//x//Down', 'Position', 'Down',1,img)
#
# test=1
