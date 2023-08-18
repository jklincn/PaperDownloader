# 知网/万方论文批量下载

使用 selenium 自动化工具模拟用户下载。

**注意：本项目不提供任何数据库下载账号，需要使用者自行准备。代码开源，保证不会窃取账号信息。**

浏览器目前支持：[Google Chrome](https://www.google.com/chrome/)

数据库目前支持：[知网](https://www.cnki.net/)、[万方](https://www.wanfangdata.com.cn/)

## 运行方法

### 可执行文件（无需安装环境，推荐）

1. 前往 release 页面下载最新文件
2. 下载浏览器版本对应驱动（WebDriver），参考 [WebDriver 下载地址](#webdriver 下载地址)
3. 将可执行文件与驱动放在同一文件夹下。
4. 运行程序

### 脚本（需要有 python 环境）

1. 下载本项目代码，有以下两种方法：

   - 使用 Git 克隆项目

     ```
     git clone https://github.com/jklincn/PaperDownloader.git
     ```

   - 在 GitHub 界面选择 Download ZIP，再解压

2. 在 PaperDownloader 文件夹中打开终端，执行

   ```
   pip install selenium==4.11.2
   python gui.py
   ```

## 使用帮助

### 具体步骤

1. 通过界面右侧按钮打开一个浏览器。
2. 在浏览器中打开相应数据库网站，登陆并检索所需内容，在需要下载的论文前面打上勾。
3. 点击界面右侧【下载】按钮，开始自动模拟下载，等待下载结束。

### 参数设置

**默认情况下无需改动**。点击界面右侧【设置】按钮，即可打开设置面板。

目前支持设置的参数有：

- Google Chrome 可执行文件路径
- 下载间隔时间

## 演示视频



## WebDriver 下载地址

### Google Chrome

【设置-关于 Chrome】中可以查看 Google Chrome 版本号，在下面链接中寻找对应的 chromedriver 。

新版本：https://googlechromelabs.github.io/chrome-for-testing/

老版本：https://chromedriver.storage.googleapis.com/index.html

## 可执行文件打包命令

```
pyinstaller -Fw --clean -n PaperDownloader -i icon.ico gui.py
```

## 更新日志

2023-08-18：加入 GUI，打包成 EXE。

2023-08-17：支持万方数据库，并且支持同时下载多个数据库，完善错误检查。

2023-08-16：第一版发布，使用谷歌浏览器批量下载知网论文。

## 未来工作

未来工作取决于大家的需求反馈，可以通过 issue 或者 email 来提出需求。

- [ ] 支持多种浏览器（Microsoft Edge、Mozilla Firefox等）
- [ ] 支持多类数据库（**万方（已支持）**、维普等）
- [x] 方便使用的图形用户界面
- [ ] 支持使用默认用户数据文件（这样可以使用原已保存在浏览器中的账号密码，快速登录知网）
- [x] 更完善的操作错误检查提示
- [ ] 支持 CAJ 下载（当 PDF 不可用时）
- [ ] GitHub WorkFlow 自动打包 EXE
- [ ] 自动下载对应浏览器版本的 WebDriver

## 已知问题

1. 问题：如果下载间隔过小，短时间下载次数过多，有可能引发知网反爬机制（需要输入验证码或者拖动图形等）。

   解决方法：增加下载间隔时间，分散下载操作。

2. 问题：使用脚本后，有可能会在桌面创建 Google Chrome 的快捷方式。

   解决方法：浏览器默认设置问题，暂未解决。目前手动删除即可。

## 联系方式

E-mail：jklincn@outlook.com

