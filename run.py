from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import sys
import shutil
import time

# Parameters
ChromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
Interval = 3
TempUserDateDir = os.getcwd() + "/chrome_temp_data"


def prepare():
    assert os.path.exists(
        ChromePath), "Can't find chrome.exe, please manually set ChromePath."
    # Create temporary folder
    if os.path.exists(TempUserDateDir):
        print("INFO: Using existing temporary user data: " + TempUserDateDir)
    else:
        print("INFO: Creating temporary user data: " + TempUserDateDir)
        os.makedirs(TempUserDateDir)
    # Open Browser
    os.popen("\""+ChromePath + "\"" + " --remote-debugging-port=16888" +
             " --user-data-dir=" + TempUserDateDir)


def download():
    # Set browser options
    ChromeOptions = webdriver.ChromeOptions()
    ChromeOptions.add_experimental_option("debuggerAddress", "127.0.0.1:16888")
    driver = webdriver.Chrome(options=ChromeOptions)
    # Find original window and save handle
    all_handles = driver.window_handles
    for handle in all_handles:
        driver.switch_to.window(handle)
        if driver.title == u"检索-中国知网":
            index_window = driver.current_window_handle
            break
    result = driver.find_element(
        By.CLASS_NAME, "result-table-list").find_element(By.TAG_NAME, "tbody")
    rows = result.find_elements(By.TAG_NAME, "tr")
    count = 0
    for i in range(len(rows)):
        # Determine if selected
        if not rows[i].find_element(By.CLASS_NAME, "cbItem").is_selected():
            continue
        rows[i].find_element(By.CLASS_NAME, "fz14").click()
        wait = WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(len(all_handles) + 1))
        # Switch to new window
        driver.switch_to.window(driver.window_handles[-1])
        wait = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "pdfDown")))
        driver.find_element(By.ID, "pdfDown").click()
        driver.close()
        # Switch back to index
        driver.switch_to.window(index_window)
        count = count + 1
        time.sleep(Interval)
    print("Download completed, total number of papers:", count)


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
