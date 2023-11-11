import shutil
import requests
import json
import zipfile
import os
from win32com import client as win_client


def get_major_minor_build(version):
    version = version.split(".")
    version.pop()
    str = ".".join(version)
    return str


def chrome(browse):
    win_obj = win_client.Dispatch("Scripting.FileSystemObject")
    current_version = get_major_minor_build(
        win_obj.GetFileVersion(browse.exe_path).strip()
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
                        if r.status_code != 200:
                            error = "chromedriver 下载请求错误\n当前工作路径：{}\n浏览器版本：{}\n驱动版本请求URL：{}\n驱动版本：{}\n驱动下载请求URL：{}".format(
                                os.getcwd(),
                                current_version,
                                request_url,
                                driver_version,
                                url,
                            )
                            return error
                        with open(path, "wb") as f:
                            shutil.copyfileobj(r.raw, f)
                    with zipfile.ZipFile(path, "r") as zip_ref:
                        zip_ref.extractall()
                    shutil.move("chromedriver-win64/chromedriver.exe", ".")
                    shutil.move(path, "chromedriver-win64")
                    shutil.rmtree("chromedriver-win64")
                    return
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
        if r.status_code != 200:
            error = "chromedriver 下载请求错误\n当前工作路径：{}\n浏览器版本：{}\n驱动版本请求URL：{}\n驱动版本：{}\n驱动下载请求URL：{}".format(
                os.getcwd(), current_version, request_url, driver_version, url
            )
            return error
        with open(path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall("chromedriver.exe")
    if os.path.exists("chromedriver.exe"):
        os.remove(path)
        return "chromedriver.exe"
    else:
        return "解压失败"


# 成功则返回驱动名，失败则返回错误信息
def get_driver(browse):
    if browse.name == "Google Chrome":
        driver_name = "chromedriver.exe"
        if os.path.exists(driver_name):
            return driver_name
        return chrome(browse)
    else:
        return None
