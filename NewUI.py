import sys
from pathlib import Path

from logger_tt import setup_logging, logger
from platformdirs import user_log_dir

from controllers.app_controller import AppController

if __name__ == "__main__":
    current_file_path = Path(__file__).resolve()
    log_path = Path(user_log_dir(), "NewUI.log")

    setup_logging(
        full_context=1,
        log_path=str(log_path),
        capture_print=True,
        config_path=str(current_file_path.parent / "log_config.json"),
    )

    app_controller = AppController()
    sys.exit(app_controller.run())
