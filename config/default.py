import os
# Default values for production
TESTING = False
DEBUG_LEVEL = "CRITICAL"

# setting instance folder for standard usecases
if os.path.exists("/lifetracker"):
    INSTANCE_FOLDER = "/lifetracker"
else:
    INSTANCE_FOLDER = os.getcwd() + "/instance"
print("Current directory" + INSTANCE_FOLDER)
