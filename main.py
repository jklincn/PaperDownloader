import time
import traceback

import config
import core


def input_int() -> int:
    while True:
        try:
            user_input = int(input("请输入一个整数: "))
            return user_input
        except ValueError:
            print("错误: 请输入一个有效的整数。")


if __name__ == "__main__":

    browse: core.Browse

    print("=======================================")
    print("欢迎使用论文批量下载器 PaperDownloader")
    print(f"当前版本: {config.VERSION}")
    print("=======================================")

    # 选择浏览器
    print("请选择使用的浏览器:")
    print(f"1: {config.ChromeName}")
    print(f"2: {config.EdgeName}")
    print("")
    user_input = input_int()
    match user_input:
        case 1:
            print("使用浏览器: Google Chrome")
            browse = core.Chrome()
        case 2:
            print("使用浏览器: Microsoft Edge")
            browse = core.Edge()
        case _:
            exit("错误: 浏览器选择错误")
    try:
        # 检查 webdriver
        print("=======================================")
        print("查找可执行文件......", end="")
        browse.check_exe_path()
        print("=======================================")
        print("查找 WebDriver......", end="", flush=True)
        browse.check_driver()
        print("=======================================")
        print("即将打开浏览器......", end="")
        for t in range(3, 0, -1):
            print(t, end="", flush=True)
            time.sleep(1)
        print()
        browse.open()
        while True:
            print("=======================================")
            # fmt: off
            input("请登录数据库网站进行内容检索, 在需要下载的论文前面打上勾，完成后输入回车键开始下载")
            # fmt: on
            print("=======================================")
            core.download(browse.driver())
            print("=======================================")
            print("本次下载结束，默认等待下一轮下载，可以使用 Ctrl+C 退出", flush=True)
    except Exception as e:
        print("程序发生异常，以下为异常信息", flush=True)
        print("=======================================", flush=True)
        traceback.print_exc()
        print(f"版本信息: {core.get_version(browse.name, browse.exe_path)}")
        print("=======================================")
        print("在反馈时请务必提供以上所有异常信息，这将有助于问题分析")
    except KeyboardInterrupt:
        print("\n程序退出")
