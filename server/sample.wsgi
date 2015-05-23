import sys
sys.path.insert(0, "/absolute/path/to/project")

activate_this = "/absolute/path/env/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

# app object is a Flask object
# must be called application

from app import app as application
