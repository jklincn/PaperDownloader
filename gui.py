import core
import sys
import ctypes
import time
import driver_helper
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from threading import Thread
from functools import partial

VERSION = "v1.1.0"


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, str):
        self.text_space.insert("end", str)
        self.text_space.update()

    def flush(self):
        pass


def window_set_to_center(win):
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    w = 800
    h = 600
    win.geometry("%dx%d+%d+%d" % (w, h, (sw - w) / 2, (sh - h) / 2))
    # win.resizable(0, 0)


def high_resolution(win):
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 获取屏幕的缩放因子
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # 设置程序缩放
    win.tk.call("tk", "scaling", ScaleFactor / 75)


def check_browse_alive(t_browse: Thread):
    while 1:
        if not t_browse.is_alive():
            print("检测到浏览器已关闭。\n")
            b_download["state"] = DISABLED
            b_get_driver["state"] = DISABLED
            b_clean["state"] = NORMAL
            b_setting["state"] = NORMAL
            return
        time.sleep(0.1)


def bf_browse(browse_name):
    global browse
    if browse_name == "chrome":
        print("使用浏览器: Google Chrome。\n")
        browse = core.Chrome(ChromePath)
    else:
        print("错误：不支持的浏览器\n")
    if browse.check():
        t_browse = Thread(target=browse.open, daemon=True)
        t_browse.start()
        t_browse_alive = Thread(target=check_browse_alive, args=[t_browse], daemon=True)
        t_browse_alive.start()
        b_download["state"] = NORMAL
        b_clean["state"] = DISABLED
        b_setting["state"] = DISABLED
        b_get_driver["state"] = NORMAL
        print("请登录数据库网站进行内容检索, 在需要下载的论文前面打上勾, 点击【下载】按钮。\n")
    else:
        print("错误: 找不到 {}.exe, 请手动设置可执行文件路径。\n".format(browse.name))


def bf_download():
    core.download(browse.driver(), int(Interval))


def bf_exit():
    win.destroy()


def log_bar(win):
    output = scrolledtext.ScrolledText(win, font=("微软雅黑", 12), width=1)
    output.pack(expand=True, fill=BOTH, side=LEFT)
    sys.stdout = StdoutRedirector(output)
    print("=======================================")
    print("欢迎使用论文批量下载器！")
    print("当前版本: {}".format(VERSION))
    print("=======================================")
    print("由于作者水平原因(为了自适应高分辨率), 请自行缩放窗口大小并拖动到合适位置")
    print("=======================================\n")
    print("请在右侧选择使用的浏览器。\n")


def bf_setting():
    win_setting = Toplevel()
    win_setting.title("设置")
    window_set_to_center(win_setting)

    value = {
        "chrome_path": StringVar(value=ChromePath),
        "interval": StringVar(value="3"),
    }

    # Google Chrome 可执行文件路径
    f_chrome_path = ttk.Frame(win_setting)
    f_chrome_path.pack(padx=20, expand=True)
    ttk.Label(f_chrome_path, text="Google Chrome 可执行文件路径: ", font=("微软雅黑", 12)).pack(
        side=LEFT
    )
    Entry(
        f_chrome_path, textvariable=value["chrome_path"], font=("微软雅黑 12"), width=60
    ).pack(side=LEFT)

    # 下载间隔时间
    f_interval = ttk.Frame(win_setting)
    f_interval.pack(padx=20, expand=True)
    ttk.Label(f_interval, text="下载间隔时间(秒): ", font=("微软雅黑", 12)).pack(side=LEFT)
    Entry(f_interval, textvariable=value["interval"], width=10, font=("微软雅黑 12")).pack(
        side=LEFT
    )

    # 确定按钮
    ttk.Button(
        win_setting, text="确定", command=partial(bf_setting_done, win_setting, value)
    ).pack(expand=True)


def bf_setting_done(win_setting, value):
    global ChromePath
    ChromePath = value["chrome_path"].get()
    Interval = value["interval"].get()
    win_setting.destroy()


def bf_clean():
    core.Chrome().clean()
    print("浏览器所有设置已重置, 用户数据已清理。\n")


def bf_get_driver():
    global browse
    print("正在自动获取 WebDriver。\n")
    file = driver_helper.get_driver(browse)
    if not file == None:
        print("已自动下载 {}。\n".format(file))
    else:
        print("错误: 无法自动下载 WebDriver。\n")


if __name__ == "__main__":
    win = Tk()
    win.title("论文批量下载器")

    browse: core.Browse = None
    ChromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    Interval = "3"

    # todo：适配高分辨率
    high_resolution(win)

    # 设置窗口大小与位置
    window_set_to_center(win)

    log_bar(win)

    browse_frame = ttk.Frame(win)
    browse_frame.pack(padx=20, pady=20, expand=True)
    ttk.Label(browse_frame, text="可选浏览器", font=("微软雅黑", 15)).pack()

    # 按钮组
    # Google Chrome
    b_google_chrome = ttk.Button(
        browse_frame, text="Google Chrome", command=partial(bf_browse, "chrome")
    )
    b_google_chrome.pack(padx=20, pady=20, expand=True, ipadx=20)
    # 获取 WebDriver
    b_get_driver = ttk.Button(
        win, text="获取 WebDriver", state=DISABLED, command=bf_get_driver
    )
    b_get_driver.pack(padx=20, pady=20, expand=True, ipadx=20)
    # 下载
    b_download = ttk.Button(win, text="下载", state=DISABLED, command=bf_download)
    b_download.pack(padx=20, pady=20, expand=True)
    # 设置
    b_setting = ttk.Button(win, text="设置", command=bf_setting)
    b_setting.pack(padx=20, pady=20, expand=True)
    # 浏览器重置
    b_clean = ttk.Button(win, text="浏览器重置", command=bf_clean)
    b_clean.pack(padx=20, pady=20, expand=True)
    # 退出
    b_exit = ttk.Button(win, text="退出", command=bf_exit)
    b_exit.pack(padx=20, pady=20, expand=True)

    win.mainloop()
