**2024.07.26 测试可正常使用**

# 知网论文批量下载

本项目使用 selenium 自动化工具模拟用户下载，旨在避免安装“知网研学”客户端来完成批量下载的功能。

**注意：本项目不提供任何数据库下载账号，需要使用者自行准备。代码开源，保证不会窃取账号信息。**

浏览器目前支持：[Google Chrome](https://www.google.com/chrome/)、[Microsoft Edge](https://www.microsoft.com/edge)

数据库目前支持：[知网](https://www.cnki.net/)、[万方](https://www.wanfangdata.com.cn/)

## 使用方法

1. 运行程序

   ```
   git clone https://github.com/jklincn/PaperDownloader.git
   cd PaperDownloader
   pip install -r requirements.txt
   python main.py
   ```

2. 根据提示选择浏览器

3. 在浏览器中打开相应数据库网站，**登陆**并检索所需内容，在需要下载的论文前面打上勾。

4. 在程序界面输入回车，开始自动模拟下载，等待下载结束。

## 配置文件

**默认情况下无需改动，当脚本发生相关错误时再进行更改**

目前参数有：

- Interval - 下载间隔时间（秒）
- WaitTime - 下载超时时间（秒）
- Chrome 浏览器相关
  - ChromeName - 浏览器名称
  - ChromePath - 浏览器可执行文件路径
  - ChromeDebugPort - 浏览器调试端口
  - ChromeDriverName - WebDriver 文件名
  - ChromeUserDataPath - 浏览器用户数据临时保存路径
- Edge 浏览器相关
  - EdgeName - 浏览器名称
  - EdgePath - 浏览器可执行文件路径
  - EdgeDebugPort - 浏览器调试端口
  - EdgeDriverName - WebDriver 文件名
  - EdgeUserDataPath - 浏览器用户数据临时保存路径

## 已知问题

1. 问题：使用脚本后，有可能会在桌面创建浏览器的快捷方式。

   解决方法：浏览器默认设置问题，暂未解决。目前需要手动删除。

2. 问题：自动下载论文中弹出下载对话框（例如询问是保存文件还是打开文件）

   解决方法：在浏览器的下载设置中关闭【每次下载都询问我该做些什么】类似选项。

## 联系方式

E-mail：jklincn@outlook.com

