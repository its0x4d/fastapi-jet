import os

# Define the directory where the "project" and "app" templates are stored.
# This is done by joining the directory of the current file (__file__) and the "templates" directory.
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")

# Get the current working directory. This is typically the directory
# that the command line is running from.
PROJECT_ROOT = os.getcwd()

# Define the base path of the project.
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
