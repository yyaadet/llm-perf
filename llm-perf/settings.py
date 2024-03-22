from pathlib import Path
import os
import logging


logging.basicConfig(level=logging.INFO, filename="debug.log", filemode="w", format="%(asctime)s-%(levelname)s %(filename)s:%(lineno)s:: %(message)s")


BASE_DIR = Path(os.path.dirname(__file__))

CEVAL_TEST_PROMPT = BASE_DIR / "../datasets/ceval/ceval.json"

REPORT_DIR = BASE_DIR / "../reports/"
if REPORT_DIR.exists() is False:
    REPORT_DIR.mkdir(parents=True)

CHROME_DRIVER = BASE_DIR / "drivers/chrome/chromedriver"
CHROME = BASE_DIR / "drivers/chrome/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME_USER_DATA = BASE_DIR / "drivers/chrome_selenium"


FIREFOX_DRIVER = BASE_DIR / "drivers/firefox/geckodriver"
FIREFOX = BASE_DIR / "drivers/firefox/Firefox.app/Contents/MacOS/firefox"
