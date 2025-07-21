from pathlib import Path
import logging
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / f"log_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_logger(name="default_logger", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
