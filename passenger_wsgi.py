import sys
import os

# Ensure the app's directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from project_registry.web import app as application
