
def base_path():
    """Returns the configured base path for data storage. Raises RuntimeError
    if the path has not been configured yet.
    """

    if BASE_PATH is None:
        raise RuntimeError('data storage base path has not been configured')

    return BASE_PATH

import sys
sys.path.append('../../')
from RR2021.paths import *
from .pipeline import DataPipeline
from .loader import register_data_loader, ImageDataLoader, LundatronLoader, GCamDataLoader

BASE_PATH = DATA_FOLDER

def configure(base_path):
    """Select the base path for data storage. This path should contain one
    folder per diagnostic.
    """

    global BASE_PATH
    BASE_PATH = base_path

# add an item for each diagnostic below...

register_data_loader('espec1', ImageDataLoader)
register_data_loader('espec2', ImageDataLoader)
register_data_loader('SideShamrock', ImageDataLoader)
register_data_loader('GammaProfile', ImageDataLoader)
register_data_loader('F40Leakage', GCamDataLoader)
