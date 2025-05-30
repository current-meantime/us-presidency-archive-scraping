import logging
import os

def setup_logging(log_file="scraping.log", error_log_file="errors.log"):
    logging_dir = "logs"
    os.makedirs(logging_dir, exist_ok=True)
    log_file = os.path.join(logging_dir, log_file)
    error_log_file = os.path.join(logging_dir, error_log_file)

    logging.basicConfig(
        level=logging.INFO,  # logs INFO, ERROR, and higher levels (e.g., WARNING, CRITICAL)
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    # adding a specific logger for errors
    error_handler = logging.FileHandler(error_log_file, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)  # Only log ERROR and higher levels to this file
    error_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(error_handler)