import os

VERSION = "v2.0.0"

# Download interval (seconds)
Interval = "3"
# Download timeout (seconds)
WaitTime = "5"

# Chrome
ChromeName = "Google Chrome"
ChromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
ChromeDebugPort = "16889"
ChromeDriverName = "chromedriver.exe"
ChromeUserDataPath = os.environ["TEMP"] + "/chrome_temp_data"

# Edge
EdgeName = "Microsoft Edge"
EdgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
EdgeDebugPort = "16890"
EdgeDriverName = "msedgedriver.exe"
EdgeUserDataPath = os.environ["TEMP"] + "/edge_temp_data"
