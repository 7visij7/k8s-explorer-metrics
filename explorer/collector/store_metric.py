import shutil
import os

def write_to_tmp(data):
    f = open(os.environ['TMP_METRICS_FILE'], 'w')
    f.write(data)
    f.close()


def move_files():
    shutil.copy(os.environ['TMP_METRICS_FILE'], os.environ['METRICS_FILE'])


def write_metrics(data):
    write_to_tmp(data)
    move_files()
    return 'update successfull'
