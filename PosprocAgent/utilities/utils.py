# The purpose of this module is to provide settings and functions
#====================================================================
import os

from configobj import ConfigObj
from pathlib import Path

# Define location of properties file (with Triple Store and RDB settings)
PROPERTIES_FILE = os.path.abspath(os.path.join(Path(__file__).parent.parent, 'resources', 'properties.properties'))

# Initialise global variables to be read from properties file
global INPUT_DIR, OUTPUT_DIR

def printline():
    print('============================================')

def read_properties_var(props,env_name):
    # Extract environmental value
    try:
        env_value = props[env_name]
    except KeyError:
        errorstr = 'Key ' + env_name + ' is missing in properties variable'
        raise KeyError(errorstr)
    if env_value == '':
        errorstr = 'No ' + env_name + ' value has been provided in properties variable'
        raise KeyError(errorstr)
    return env_value

def read_properties_file(filepath):
    """
        Reads settings from properties file (as global variables).
    """
    # Define global scope for global variables
    global INPUT_DIR, OUTPUT_DIR
    props = ConfigObj(filepath)

    # Extract directories
    INPUT_DIR = read_properties_var(props,'INPUT_DIR')
    OUTPUT_DIR = read_properties_var(props,'OUTPUT_DIR')

# Run when module is imported
read_properties_file(PROPERTIES_FILE)