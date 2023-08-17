from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions
import os
import sys
import shutil
import time

# Parameters
ChromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
Interval = 3
TempUserDateDir = os.getcwd() + "/chrome_temp_data"
Port = "16888"
WaitTime = 5

# Global Variables
check_count = 0
download_count = 0


def prepare():
    assert os.path.exists(
        ChromePath), "ERROR: Can't find chrome.exe, please manually set ChromePath."
    # Create temporary folder
    if os.path.exists(TempUserDateDir):
        print("INFO: Using existing temporary user data: ", TempUserDateDir)
    else:
        print("INFO: Creating temporary user data: ", TempUserDateDir)
        os.makedirs(TempUserDateDir)
    # Open Browser
    os.popen("\"{}\" --remote-debugging-port={} --user-data-dir={}".format(
        ChromePath, Port, TempUserDateDir))


def download():
    # Set browser options
    ChromeOptions = webdriver.ChromeOptions()
    ChromeOptions.add_experimental_option(
        "debuggerAddress", "127.0.0.1:{}".format(Port))
    driver = webdriver.Chrome(options=ChromeOptions)
    # Find serach window
    all_handles = driver.window_handles
    hit = False

    for handle in all_handles:
        driver.switch_to.window(handle)
        if driver.title == u"检索-中国知网":
            cnki(driver)
            hit = True
        elif driver.title == u"高级检索-中国知网":
            cnki(driver)
            hit = True
        elif driver.title == u"万方数据知识服务平台":
            # Ensure we are now in search window
            try:
                driver.find_element(By.CLASS_NAME, "normal-list")
            except exceptions.NoSuchElementException:
                continue
            else:
                wanfang(driver)
                hit = True
    assert hit, "ERROR: Can't find database search window."
    print("INFO: Download completed, total number of papers: {}/{}".format(
          download_count, check_count))


def cnki(driver: webdriver.Chrome):
    print("INFO: Start downloading cnki...")
    global download_count, check_count
    index_window = driver.current_window_handle
    result = driver.find_element(
        By.CLASS_NAME, "result-table-list").find_element(By.TAG_NAME, "tbody")
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
                EC.number_of_windows_to_be(current_window_number + 1))
            # Switch to new window
            driver.switch_to.window(driver.window_handles[-1])
            WebDriverWait(driver, WaitTime).until(
                EC.element_to_be_clickable((By.ID, "pdfDown")))
            try:
                download_button = driver.find_element(By.ID, "pdfDown")
            except exceptions.NoSuchElementException:
                name = rows[i].find_element(By.CLASS, "wx-tit").text
                print("ERROR: Can't download {}.".format(name))
                continue
            else:
                current_window_number = len(driver.window_handles)
                download_button.click()
                try:
                    WebDriverWait(driver, WaitTime).until(
                        EC.number_of_windows_to_be(current_window_number))
                except exceptions.TimeoutException:
                    print("ERROR: Account not logged in.")
                    return
                else:
                    driver.close()
                    # Switch back to index
                    driver.switch_to.window(index_window)
                    download_count += 1
                    time.sleep(Interval)


def wanfang(driver: webdriver.Chrome):
    print("INFO: Start downloading wanfang...")
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
                    By.CSS_SELECTOR, "div:nth-child({}) > .normal-list .t-DIB:nth-child(2) span".format(str(i+1)))
            except exceptions.NoSuchElementException:
                name = rows[i].find_element(By.CLASS_NAME, "title").text
                print("ERROR: Can't download {}.".format(name))
                continue
            else:
                download_button.click()
                # Switch to new window
                WebDriverWait(driver, WaitTime).until(
                    EC.number_of_windows_to_be(current_window_number + 1))
                driver.switch_to.window(driver.window_handles[-1])
                if driver.title == u"万方登录":
                    print("ERROR: Account not logged in.")
                    return
                else:
                    time.sleep(Interval)
                    driver.close()
                    # Switch back to index
                    driver.switch_to.window(index_window)
                    download_count += 1


def clean():
    if os.path.exists(TempUserDateDir):
        shutil.rmtree(TempUserDateDir)


def usage():
    print("usage: python run.py <command>")
    print("Optional commands are as follows:")
    print("  prepare    Open the browser and prepare the website")
    print("  download   Start automated download")
    print("  clean      Delete temporary data directory")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "prepare":
            prepare()
        elif sys.argv[1] == "download":
            download()
        elif sys.argv[1] == "clean":
            clean()
        else:
            usage()
    else:
        usage()
