import sys

from logger_tt import setup_logging, logger

from controllers.app_controller import AppController
from utilities.path_info import PathInfo

if __name__ == "__main__":
    # One-time-initialize PathInfo object. This has to be done inside __main__ so we can use __file__.
    PathInfo(__file__)

    log_path = PathInfo().user_log_folder / "NewUI.log"
    with log_path.open("w") as file:
        pass

    config_path = PathInfo().application_folder / "log_config.json"

    setup_logging(
        full_context=1,
        log_path=str(log_path),
        capture_print=True,
        config_path=str(config_path),
    )

    app_controller = AppController()
    sys.exit(app_controller.run())
