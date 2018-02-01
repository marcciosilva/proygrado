import errno
import os

import sys


def split_list_in_chunks(lst, chunk_amount):
    """
    Splits list lst in lists of chunk_amount elements and returns them (as a list of lists)
    """
    chunk_amount = max(1, chunk_amount)
    return [lst[i:i + chunk_amount] for i in range(0, len(lst), chunk_amount)]


def generate_dir(path):
    """
    If path doesn't exist, it gets created
    """
    try:
        os.makedirs(path)
        print('Directory ' + path + ' created or already existed.')
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise


def block_console_print():
    """
    Disables printing to the console.
    """
    sys.stdout = open(os.devnull, 'w')


def enable_console_print():
    """
    Enables printing to the console.
    :return:
    """
    sys.stdout = sys.__stdout__
