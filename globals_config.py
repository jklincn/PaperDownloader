import os

VERSION = "v1.2.0"

# settings
# Download interval, Unit in seconds
Interval = "3"
# Download timeout, Unit in seconds
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
