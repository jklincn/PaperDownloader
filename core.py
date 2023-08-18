from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions
import os
import shutil
import time
import subprocess

# Parameters
WaitTime = 5

# Global Variables
check_count = 0
download_count = 0


class Browse:
    def __init__(self):
        self.name = ""
        self.exe_path = ""

    def open(self):
        pass


class Chrome(Browse):
    def __init__(self, ChromePath=""):
        self.name = "Google Chrome"
        self.exe_path = ChromePath
        self.user_data_path = os.environ["TEMP"] + "/chrome_temp_data"
        self.port = "16888"

    def open(self):
        if not os.path.exists(self.exe_path):
            print("错误: 找不到 chrome.exe, 请手动设置 ChromePath。\n")
            return
        # Create temporary folder
        if not os.path.exists(self.user_data_path):
            os.makedirs(self.user_data_path)
        subprocess.run(
            [
                self.exe_path,
                "--remote-debugging-port={}".format(self.port),
                "--user-data-dir={}".format(self.user_data_path),
            ]
        )

    def driver(self) -> webdriver:
        # Set browser options
        ChromeOptions = webdriver.ChromeOptions()
        ChromeOptions.add_experimental_option(
            "debuggerAddress", "127.0.0.1:{}".format(self.port)
        )
        service = webdriver.ChromeService(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(options=ChromeOptions,service=service)
        return driver

    def clean(self):
        if os.path.exists(self.user_data_path):
            shutil.rmtree(self.user_data_path)


def download(driver: webdriver,Interval):
    # Find serach window
    all_handles = driver.window_handles
    hit = False
    for handle in all_handles:
        driver.switch_to.window(handle)
        if driver.title == "检索-中国知网":
            cnki(driver,Interval)
            hit = True
        elif driver.title == "高级检索-中国知网":
            cnki(driver,Interval)
            hit = True
        elif driver.title == "万方数据知识服务平台":
            # Ensure we are now in search window
            try:
                driver.find_element(By.CLASS_NAME, "normal-list")
            except exceptions.NoSuchElementException:
                continue
            else:
                wanfang(driver,Interval)
                hit = True
    if hit:
        print("下载完成, 共找到 {} 处勾选, 成功下载 {} 项内容。\n".format(download_count, check_count))
    else:
        print("错误: 没有找到符合的检索页面\n")


def cnki(driver: webdriver,Interval):
    print("检测到知网检索页面, 开始下载......\n")
    global download_count, check_count
    index_window = driver.current_window_handle
    result = driver.find_element(By.CLASS_NAME, "result-table-list").find_element(
        By.TAG_NAME, "tbody"
    )
    rows = result.find_elements(By.TAG_NAME, "tr")
    for i in range(len(rows)):
        # Determine if selected
        if not rows[i].find_element(By.CLASS_NAME, "cbItem").is_selected():
            continue
        else:
            check_count += 1
            current_window_number = len(driver.window_handles)
            rows[i].find_element(By.CLASS_NAME, "fz14").click()
            WebDriverWait(driver, WaitTime).until(
                EC.number_of_windows_to_be(current_window_number + 1)
            )
            # Switch to new window
            driver.switch_to.window(driver.window_handles[-1])
            WebDriverWait(driver, WaitTime).until(
                EC.element_to_be_clickable((By.ID, "pdfDown"))
            )
            try:
                download_button = driver.find_element(By.ID, "pdfDown")
            except exceptions.NoSuchElementException:
                name = rows[i].find_element(By.CLASS, "wx-tit").text
                print("错误: 不能下载 {}\n。".format(name))
                continue
            else:
                current_window_number = len(driver.window_handles)
                download_button.click()
                try:
                    WebDriverWait(driver, WaitTime).until(
                        EC.number_of_windows_to_be(current_window_number)
                    )
                except exceptions.TimeoutException:
                    print("错误: 账号未登录，下载中断。\n")
                    return
                else:
                    driver.close()
                    # Switch back to index
                    driver.switch_to.window(index_window)
                    download_count += 1
                    time.sleep(Interval)


def wanfang(driver: webdriver,Interval):
    print("检测到万方检索页面, 开始下载......\n")
    global download_count, check_count
    index_window = driver.current_window_handle
    rows = driver.find_elements(By.CLASS_NAME, "normal-list")
    for i in range(len(rows)):
        # Determine if selected
        try:
            rows[i].find_element(By.CLASS_NAME, "checkbox.active")
        except exceptions.NoSuchElementException:
            continue
        else:
            check_count += 1
            current_window_number = len(driver.window_handles)
            try:
                download_button = rows[i].find_element(
                    By.CSS_SELECTOR,
                    "div:nth-child({}) > .normal-list .t-DIB:nth-child(2) span".format(
                        str(i + 1)
                    ),
                )
            except exceptions.NoSuchElementException:
                name = rows[i].find_element(By.CLASS_NAME, "title").text
                print("错误: 不能下载 {}。\n".format(name))
                continue
            else:
                download_button.click()
                # Switch to new window
                WebDriverWait(driver, WaitTime).until(
                    EC.number_of_windows_to_be(current_window_number + 1)
                )
                driver.switch_to.window(driver.window_handles[-1])
                if driver.title == "万方登录":
                    print("错误: 账号未登录，下载中断。\n")
                    return
                else:
                    time.sleep(Interval)
                    driver.close()
                    # Switch back to index
                    driver.switch_to.window(index_window)
                    download_count += 1


# def usage():
#     print("usage: python run.py <command>")
#     print("Optional commands are as follows:")
#     print("  prepare    Open the browser and prepare the website")
#     print("  download   Start automated download")
#     print("  clean      Delete temporary data directory")


# if __name__ == "__main__":
#     if len(sys.argv) == 2:
#         if sys.argv[1] == "prepare":
#             prepare()
#         elif sys.argv[1] == "download":
#             download()
#         elif sys.argv[1] == "clean":
#             clean()
#         else:
#             usage()
#     else:
#         usage()
