from selenium.webdriver.chrome.options import Options

CHROME_USER_DATA_DIR = "C:\\Users\\jonat\\AppData\\Local\\Google\\Chrome\\User Data"
CHROME_PROFILE_DIR = "Profile 1"
HEADLESS = True
TIMEOUT = 20

def get_chrome_options():
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"user-data-dir={CHROME_USER_DATA_DIR}")
    chrome_options.add_argument(f"profile-directory={CHROME_PROFILE_DIR}")
    return chrome_options
