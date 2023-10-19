import sys

from logger_tt import setup_logging, logger

from controllers.app_controller import AppController
from utilities.path_info import PathInfo

if __name__ == "__main__":
    # One-time-initialize PathInfo object. This has to be done inside __main__ so we can use __file__.
    PathInfo(__file__)

    setup_logging(
        full_context=1,
        log_path=str(PathInfo().log_folder / "NewUI.log"),
        capture_print=True,
        config_path=str(PathInfo().application_folder / "log_config.json"),
    )

    app_controller = AppController()
    sys.exit(app_controller.run())
