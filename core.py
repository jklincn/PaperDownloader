import os
import platform
import subprocess
import sys
import time

import pkg_resources
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import config
import driver_helper

# Global Variables
check_count = 0
download_count = 0


class Browse:
    def __init__(self):
        self.name = None
        self.exe_path = None
        self.debug_port = None
        self.driver_path = None
        self.user_data_path = None

    def open(self):
        if not os.path.exists(self.user_data_path):
            os.makedirs(self.user_data_path)
        # require new user-data-dir
        subprocess.Popen(
            [
                self.exe_path,
                f"--remote-debugging-port={self.debug_port}",
                f"--user-data-dir={self.user_data_path}",
            ]
        )

    def check_exe_path(self):
        if os.path.exists(self.exe_path):
            print("成功")
        else:
            print("失败")
            print("请检查路径：", self.exe_path)
            sys.exit("查找可执行文件失败")

    def check_driver(self):
        if os.path.exists(self.driver_path):
            print("成功")
        else:
            print("失败\n尝试自动下载 WebDriver...", end="")
            driver_helper.get_driver(self.name)
            print("成功")

    def driver(self) -> webdriver:
        pass


class Chrome(Browse):
    def __init__(self):
        self.name = config.ChromeName
        self.exe_path = config.ChromePath
        self.debug_port = config.ChromeDebugPort
        self.driver_path = config.ChromeDriverName
        self.user_data_path = config.ChromeUserDataPath

    def driver(self) -> webdriver:
        ChromeOptions = webdriver.ChromeOptions()
        ChromeOptions.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{self.debug_port}"
        )
        service = webdriver.ChromeService(executable_path=self.driver_path)
        driver = webdriver.Chrome(options=ChromeOptions, service=service)
        return driver


# https://learn.microsoft.com/en-us/microsoft-edge/devtools-protocol-chromium/
class Edge(Browse):
    def __init__(self):
        self.name = config.EdgeName
        self.exe_path = config.EdgePath
        self.debug_port = config.EdgeDebugPort
        self.driver_path = config.EdgeDriverName
        self.user_data_path = config.EdgeUserDataPath

    def driver(self) -> webdriver:
        EdgeOptions = webdriver.EdgeOptions()
        EdgeOptions.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{self.debug_port}"
        )
        service = webdriver.EdgeService(executable_path=self.driver_path)
        driver = webdriver.Edge(options=EdgeOptions, service=service)
        return driver


def download(driver: webdriver, browse_name: str):
    global download_count, check_count
    download_count = 0
    check_count = 0

    print("正在接管浏览器控制，请不要操作。", flush=True)
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
        # fmt: off
        print(f"下载完成, 共找到 {check_count} 处勾选, 成功下载 {download_count} 项内容。")
        print(f"文件保存位置: {os.path.join(os.environ['USERPROFILE'], 'Downloads')}")
        # fmt: on
    else:
        print("错误：没有找到符合的检索页面\n")


def cnki(driver: webdriver, browse_name: str):
    global download_count, check_count
    print("检测到知网检索页面, 开始下载......")
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
            WebDriverWait(driver, int(config.WaitTime)).until(
                EC.number_of_windows_to_be(current_window_number + 1)
            )
            # Switch to new window
            driver.switch_to.window(driver.window_handles[-1])
            download_button = WebDriverWait(driver, int(config.WaitTime)).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//li[@class="btn-dlpdf"]//a[@id="cajDown"] | //li[@class="btn-dlpdf"]//a[@id="pdfDown"]',
                    )
                )
            )
            download_button.click()
            current_window_number = len(driver.window_handles)
            # edge 的 webdriver 有问题，页面关闭后数量不减
            if browse_name == config.EdgeName:
                time.sleep(int(config.Interval))
                driver.close()
                driver.switch_to.window(index_window)
                download_count += 1
            else:
                try:
                    WebDriverWait(driver, int(config.WaitTime)).until(
                        EC.number_of_windows_to_be(current_window_number)
                    )
                except exceptions.TimeoutException:
                    print("错误：账号未登录或响应超时，下载中断。\n")
                    return
                driver.close()
                # Switch back to index
                driver.switch_to.window(index_window)
                download_count += 1
                time.sleep(int(config.Interval))


def wanfang(driver: webdriver):
    global download_count, check_count
    print("检测到万方检索页面, 开始下载......")
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
                    f"div:nth-child({str(i + 1)}) > .normal-list .t-DIB:nth-child(2) span",
                )
            except exceptions.NoSuchElementException:
                name = rows[i].find_element(By.CLASS_NAME, "title").text
                print(f"错误：不能下载 {name}。\n")
                continue

            download_button.click()
            # Switch to new window
            WebDriverWait(driver, int(config.WaitTime)).until(
                EC.number_of_windows_to_be(current_window_number + 1)
            )
            driver.switch_to.window(driver.window_handles[-1])
            if driver.title == "万方登录":
                print("错误：账号未登录或响应超时，下载中断。\n")
                return
            elif driver.title == "万方数据知识服务平台-无权限访问":
                print("错误：账号无权限。\n")
                return
            else:
                time.sleep(int(config.Interval))
                driver.close()
                # Switch back to index
                driver.switch_to.window(index_window)
                download_count += 1


def get_version(browse_name: str, browse_path: str) -> str:
    version = "\n"
    version += f"PaperDownloader: {config.VERSION}\n"
    version += f"Python: {platform.python_version()}\n"
    packages = ["selenium"]
    for pkg in packages:
        try:
            version = pkg_resources.get_distribution(pkg).version
            version += f"{pkg}: {version}\n"
        except pkg_resources.DistributionNotFound:
            version += f"{pkg} not install\n"
    version += f"{browse_name}: {driver_helper.get_version(browse_path)}"
    return version
