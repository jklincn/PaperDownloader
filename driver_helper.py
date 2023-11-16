import shutil
import requests
import json
import zipfile
import os
import globals_config
from win32com import client as win_client


def get_major_minor_build(version):
    version = version.split(".")
    version.pop()
    str = ".".join(version)
    return str


# https://chromedriver.chromium.org/downloads
def chrome():
    # Delete old WebDriver
    if os.path.exists(globals_config.ChromeDriverName):
        os.remove(globals_config.ChromeDriverName)
    win_obj = win_client.Dispatch("Scripting.FileSystemObject")
    current_version = get_major_minor_build(
        win_obj.GetFileVersion(globals_config.ChromePath).strip()
    )
    latest_json = json.loads(
        requests.get(
            "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
        ).text
    )
    for channels in latest_json["channels"]:
        version = get_major_minor_build(latest_json["channels"][channels]["version"])
        if current_version == version:
            for platform in latest_json["channels"][channels]["downloads"][
                "chromedriver"
            ]:
                if platform["platform"] == "win64":
                    url = platform["url"]
                    path = "chromedriver-win64.zip"
                    with requests.get(url, stream=True) as r:
                        with open(path, "wb") as f:
                            shutil.copyfileobj(r.raw, f)
                    with zipfile.ZipFile(path, "r") as zip_ref:
                        zip_ref.extractall()
                    shutil.move("chromedriver-win64/chromedriver.exe", ".")
                    shutil.move(path, "chromedriver-win64")
                    shutil.rmtree("chromedriver-win64")
                    return globals_config.ChromeDriverName
    request_url = (
        "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + current_version
    )
    driver_version = requests.get(request_url).text
    url = (
        "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(
            driver_version
        )
    )
    path = "chromedriver-win32.zip"
    with requests.get(url, stream=True) as r:
        with open(path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(globals_config.ChromeDriverName)
    os.remove(path)


# https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#downloads
def edge():
    # Delete old WebDriver
    if os.path.exists(globals_config.EdgeDriverName):
        os.remove(globals_config.EdgeDriverName)
    win_obj = win_client.Dispatch("Scripting.FileSystemObject")
    current_version = win_obj.GetFileVersion(globals_config.EdgePath).strip()
    url = "https://msedgedriver.azureedge.net/{}/edgedriver_win64.zip".format(
        current_version
    )
    path = "edgedriver_win64.zip"
    with requests.get(url, stream=True) as r:
        with open(path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall()
    os.remove(path)
    return globals_config.EdgeDriverName


def get_driver(browse_name) -> str:
    match browse_name:
        case globals_config.ChromeName:
            return chrome()
        case globals_config.EdgeName:
            return edge()
        case _:
            return None
