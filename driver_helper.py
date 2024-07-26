import os
import shutil
import sys
import zipfile

import requests
from win32com import client as win_client

import config


def get_version(exe_path):
    win_obj = win_client.Dispatch("Scripting.FileSystemObject")
    version = win_obj.GetFileVersion(exe_path).strip()
    return version


# https://chromedriver.chromium.org/downloads
def chrome():
    current_version = get_version(config.ChromePath)
    url = f"https://storage.googleapis.com/chrome-for-testing-public/{current_version}/win64/chromedriver-win64.zip"
    zip_path = "chromedriver-win64.zip"
    file_path = "chromedriver-win64/" + config.ChromeDriverName
    try:
        with requests.get(url, stream=True) as r:
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            with zip_ref.open(file_path) as source_file:
                content = source_file.read()
                target_file_path = os.path.join(
                    os.getcwd(), os.path.basename(file_path)
                )
                with open(target_file_path, "wb") as target_file:
                    target_file.write(content)
        os.remove(zip_path)
    except BaseException as e:
        raise requests.exceptions.RequestException(
            f"请手动下载 {url} （可能需要科学上网）并将 {config.ChromeDriverName} 解压到当前目录"
        ) from e


# https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#downloads
def edge():
    current_version = get_version(config.EdgePath)
    url = f"https://msedgedriver.azureedge.net/{current_version}/edgedriver_win64.zip"
    zip_path = "edgedriver_win64.zip"
    try:
        with requests.get(url, stream=True) as r:
            with open(zip_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extract(config.EdgeDriverName)
        os.remove(zip_path)
    except BaseException as e:
        raise requests.exceptions.RequestException(
            f"请手动下载 {url} （可能需要科学上网）并将 {config.EdgeDriverName} 解压到当前目录"
        ) from e


def get_driver(browse_name):
    try:
        match browse_name:
            case config.ChromeName:
                chrome()
            case config.EdgeName:
                edge()
    except BaseException as e:
        sys.exit(f"失败\n{e}")
