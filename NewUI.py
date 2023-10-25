import sys

from loguru import logger

from controllers.app_controller import AppController
from utilities.app_info import AppInfo

if __name__ == "__main__":
    # One-time-initialize AppInfo object. This has to be done inside __main__ so we can use __file__.
    AppInfo(__file__)

    log_path = AppInfo().user_log_folder / f"{AppInfo().app_name}.log"
    if not AppInfo().user_log_folder.exists():
        AppInfo().user_log_folder.mkdir(parents=True, exist_ok=True)

    logger.info("Starting application")

    app_controller = AppController()
    sys.exit(app_controller.run())
