import base64
import importlib.metadata
import os
import platform
import subprocess
import sys
import time
from io import BytesIO

import ddddocr
from PIL import Image
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
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{self.debug_port}"
        )
        service = webdriver.ChromeService(executable_path=self.driver_path)
        driver = webdriver.Chrome(options=chrome_options, service=service)
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
        edge_options = webdriver.EdgeOptions()
        edge_options.add_experimental_option(
            "debuggerAddress", f"127.0.0.1:{self.debug_port}"
        )
        service = webdriver.EdgeService(executable_path=self.driver_path)
        driver = webdriver.Edge(options=edge_options, service=service)
        return driver


def download(driver: webdriver):
    global download_count, check_count
    download_count = 0
    check_count = 0

    print("正在接管浏览器控制，请不要操作。", flush=True)
    # Find serach window
    all_handles = driver.window_handles
    hit = False
    for handle in all_handles:
        driver.switch_to.window(handle)
        match driver.title:
            case "检索-中国知网" | "高级检索-中国知网":
                cnki(driver)
                hit = True
            case "万方数据知识服务平台":
                # 万方的首页和搜索页是同一个标题，因此通过寻找元素来保证当前在搜索页
                try:
                    driver.find_element(By.CLASS_NAME, "normal-list")
                except exceptions.NoSuchElementException:
                    continue
                wanfang(driver)
                hit = True

    if hit:
        # fmt: off
        print(f"下载完成, 共找到 {check_count} 处勾选, 成功下载 {download_count} 项内容。")
        print(f"文件保存位置: {os.path.join(os.environ['USERPROFILE'], 'Downloads')}")
        # fmt: on
    else:
        print("错误：没有找到符合的检索页面\n")


def cnki(driver: webdriver):
    global download_count, check_count
    print("检测到知网检索页面, 开始下载......")
    index_window = driver.current_window_handle

    trs = driver.find_elements(By.XPATH, "//*[@class='result-table-list']/tbody/tr")

    # 遍历每一个条目
    for tr in trs:
        # 判断是否选中
        if not tr.find_element(By.CLASS_NAME, "cbItem").is_selected():
            continue
        else:
            check_count += 1
            current_window_number = len(driver.window_handles)

            # 打开并切换到详情页
            tr.find_element(By.CLASS_NAME, "fz14").click()
            WebDriverWait(driver, int(config.WaitTime)).until(
                EC.number_of_windows_to_be(current_window_number + 1)
            )
            detail_window = driver.window_handles[-1]
            driver.switch_to.window(detail_window)

            # 寻找下载按钮
            download_button = WebDriverWait(driver, int(config.WaitTime)).until(
                EC.any_of(
                    EC.element_to_be_clickable(
                        # https://github.com/jklincn/PaperDownloader/issues/6
                        (By.XPATH, '//li[@class="btn-dlpdf"]//a[@id="cajDown"]')
                    ),
                    EC.element_to_be_clickable(
                        (By.XPATH, '//li[@class="btn-dlpdf"]//a[@id="pdfDown"]')
                    ),
                )
            )
            # 记录当前窗口数量
            current_window_number = len(driver.window_handles)

            # 点击下载按钮
            download_button.click()

            # 等待页面打开
            WebDriverWait(driver, int(config.WaitTime)).until(
                EC.number_of_windows_to_be(current_window_number + 1)
            )
            driver.switch_to.window(driver.window_handles[-1])

            # Todo: 对各类错误的处理，比如产品不在有效期范围之内和重新登陆。

            # 处理滑动验证码
            if driver.title == "滑动验证":
                cnki_slide_verify(driver)
                driver.close()

            # 关闭详情页
            driver.switch_to.window(detail_window)
            driver.close()

            # 切换回检索页面
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
    packages = ["selenium", "ddddocr"]
    for pkg in packages:
        try:
            pkg_version = importlib.metadata.version(pkg)
            version += f"{pkg}: {pkg_version}\n"
        except importlib.metadata.PackageNotFoundError:
            version += f"{pkg} not install\n"
    version += f"{browse_name}: {driver_helper.get_version(browse_path)}"
    return version


def cnki_slide_verify(driver: webdriver):
    while True:

        # 等待加载
        time.sleep(1)

        # 获取背景图片并转换成字节
        try:
            background = WebDriverWait(driver, int(config.WaitTime)).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='verify-img-panel']/img")
                )
            )
        except exceptions.TimeoutException:
            print("滑动验证码错误，自动重试......")
            continue
        background_src = background.get_attribute("src")
        _, base64_str = background_src.split(",", 1)
        background_bytes = base64.b64decode(base64_str)

        # 计算图片缩放比例
        rendered_width = background.size["width"]
        img = Image.open(BytesIO(background_bytes))
        intrinsic_width, _ = img.size
        width_scale = rendered_width / intrinsic_width

        # 获取缺口图片并转换成字节
        target = WebDriverWait(driver, int(config.WaitTime)).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='verify-sub-block']/img")
            )
        )
        target_src = target.get_attribute("src")
        _, base64_str = target_src.split(",", 1)
        target_bytes = base64.b64decode(base64_str)

        # 使用 ddddocr 库进行处理
        det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        res = det.slide_match(target_bytes, background_bytes)

        # 计算滑动距离
        x_move_length = width_scale * res["target"][0] - 2  # 2 是观察所得的修正值

        # 找到滑动按钮
        slider = driver.find_element(By.XPATH, "//div[@class='verify-move-block']")

        # 使用 ActionChains 拖动滑块
        action = webdriver.ActionChains(driver)
        action.click_and_hold(slider).perform()
        action.move_by_offset(x_move_length, 0).perform()
        time.sleep(0.5)
        action.release().perform()

        # 判断是否成功
        try:
            element = WebDriverWait(driver, int(config.WaitTime)).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/h4"))
            )
            if element.text == "验证成功，请稍等，正在下载中...":
                return
            else:
                print("错误：滑动验证码处理错误")
        except exceptions.TimeoutException:
            print("滑动验证码错误，自动重试......")
            continue
