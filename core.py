# pyinstaller -Fw --clean -n PaperDownloader -i icon.ico gui.py
import os
import shutil
import time
import subprocess
import globals_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions

# Global Variables
check_count = 0
download_count = 0


class Browse:
    def __init__(self):
        self.name = None
        self.exe_path = None
        self.user_data_path = None
        self.debug_port = None

    def open(self):
        pass

    def driver(self) -> webdriver:
        pass

    def check(self) -> bool:
        if os.path.exists(self.exe_path):
            return True
        else:
            return False

    def clean(self):
        if os.path.exists(self.user_data_path):
            shutil.rmtree(self.user_data_path)


class Chrome(Browse):
    def __init__(self):
        self.name = globals_config.ChromeName
        self.exe_path = globals_config.ChromePath
        self.user_data_path = globals_config.ChromeUserDataPath
        self.debug_port = globals_config.ChromeDebugPort

    def open(self):
        # Create temporary folder
        if not os.path.exists(self.user_data_path):
            os.makedirs(self.user_data_path)
        subprocess.run(
            [
                self.exe_path,
                "--remote-debugging-port={}".format(self.debug_port),
                "--user-data-dir={}".format(self.user_data_path),
            ]
        )

    def driver(self) -> webdriver:
        # Set browser options
        ChromeOptions = webdriver.ChromeOptions()
        ChromeOptions.add_experimental_option(
            "debuggerAddress", "127.0.0.1:{}".format(self.debug_port)
        )
        service = webdriver.ChromeService(
            executable_path=globals_config.ChromeDriverName
        )
        try:
            driver = webdriver.Chrome(options=ChromeOptions, service=service)
        except exceptions.NoSuchDriverException:
            print("错误：找不到 WebDriver 文件。请先点击右侧【获取 WebDriver】按钮。\n")
            return None
        else:
            return driver


# https://learn.microsoft.com/en-us/microsoft-edge/devtools-protocol-chromium/
class Edge(Browse):
    def __init__(self):
        self.name = globals_config.EdgeName
        self.exe_path = globals_config.EdgePath
        self.user_data_path = globals_config.EdgeUserDataPath
        self.debug_port = globals_config.EdgeDebugPort

    def open(self):
        # Create temporary folder
        if not os.path.exists(self.user_data_path):
            os.makedirs(self.user_data_path)
        subprocess.run(
            [
                self.exe_path,
                "--remote-debugging-port={}".format(self.debug_port),
                "--user-data-dir={}".format(self.user_data_path),
            ]
        )

    def driver(self) -> webdriver:
        # Set browser options
        EdgeOptions = webdriver.EdgeOptions()
        EdgeOptions.add_experimental_option(
            "debuggerAddress", "127.0.0.1:{}".format(self.debug_port)
        )
        service = webdriver.EdgeService(executable_path=globals_config.EdgeDriverName)
        try:
            driver = webdriver.Edge(options=EdgeOptions, service=service)
        except exceptions.NoSuchDriverException:
            print("错误：找不到 WebDriver 文件。请先点击右侧【获取 WebDriver】按钮。\n")
            return None
        else:
            return driver


def download(driver: webdriver, browse_name: str):
    global download_count, check_count
    download_count = 0
    check_count = 0
    if driver == None:
        return
    else:
        print("正在接管浏览器控制，请不要操作。\n", flush=True)
        # Find serach window
        all_handles = driver.window_handles
        hit = False
        for handle in all_handles:
            driver.switch_to.window(handle)
            if driver.title == "检索-中国知网" or driver.title == "高级检索-中国知网":
                cnki(driver, browse_name)
                hit = True
            elif driver.title == "万方数据知识服务平台":
                # Ensure we are now in search window
                try:
                    driver.find_element(By.CLASS_NAME, "normal-list")
                except exceptions.NoSuchElementException:
                    continue
                else:
                    wanfang(driver)
                    hit = True
        if hit:
            print(
                "下载完成, 共找到 {} 处勾选, 成功下载 {} 项内容。\n".format(check_count, download_count)
            )
        else:
            print("错误：没有找到符合的检索页面\n")
        print("浏览器接管结束, 可以继续操作。\n", flush=True)


def cnki(driver: webdriver, browse_name: str):
    global download_count, check_count
    print("检测到知网检索页面, 开始下载......\n")
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
            WebDriverWait(driver, int(globals_config.WaitTime)).until(
                EC.number_of_windows_to_be(current_window_number + 1)
            )
            # Switch to new window
            driver.switch_to.window(driver.window_handles[-1])
            WebDriverWait(driver, int(globals_config.WaitTime)).until(
                EC.element_to_be_clickable((By.ID, "pdfDown"))
            )
            try:
                download_button = driver.find_element(By.ID, "pdfDown")
            except exceptions.NoSuchElementException:
                name = rows[i].find_element(By.CLASS, "wx-tit").text
                print("错误：不能下载 {}\n。".format(name))
                continue
            else:
                current_window_number = len(driver.window_handles)
                download_button.click()
                # edge 的 webdriver 有问题，页面关闭后数量不减
                if browse_name == globals_config.EdgeName:
                    time.sleep(int(globals_config.Interval))
                    driver.close()
                    driver.switch_to.window(index_window)
                    download_count += 1
                else:
                    try:
                        WebDriverWait(driver, int(globals_config.WaitTime)).until(
                            EC.number_of_windows_to_be(current_window_number)
                        )
                    except exceptions.TimeoutException:
                        print("错误：账号未登录或响应超时，下载中断。\n")
                        return
                    else:
                        driver.close()
                        # Switch back to index
                        driver.switch_to.window(index_window)
                        download_count += 1
                        time.sleep(int(globals_config.Interval))


def wanfang(driver: webdriver):
    global download_count, check_count
    print("检测到万方检索页面, 开始下载......\n")
    index_window = driver.current_window_handle
    rows = driver.find_elements(By.CLASS_NAME, "normal-list")
    for i in range(len(rows)):
        # Determine if selected
        if not rows[i].find_element(By.CLASS_NAME, "ivu-checkbox-input").is_selected():
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
                print("错误：不能下载 {}。\n".format(name))
                continue
            else:
                download_button.click()
                # Switch to new window
                WebDriverWait(driver, int(globals_config.WaitTime)).until(
                    EC.number_of_windows_to_be(current_window_number + 1)
                )
                driver.switch_to.window(driver.window_handles[-1])
                if driver.title == "万方登录":
                    print("错误：账号未登录或响应超时，下载中断。\n")
                    return
                else:
                    time.sleep(int(globals_config.Interval))
                    driver.close()
                    # Switch back to index
                    driver.switch_to.window(index_window)
                    download_count += 1
