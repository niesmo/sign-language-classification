import logging
import logging.config
import sys, os, inspect

curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
logging_config_file = os.path.abspath(os.path.join(curr_dir, '../config/logging.conf'))

logging.config.fileConfig(logging_config_file)