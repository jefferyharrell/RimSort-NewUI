import sys

from controllers.app_controller import AppController

if __name__ == "__main__":
    app_controller = AppController()
    sys.exit(app_controller.run())
