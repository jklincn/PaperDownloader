# 知网/万方论文批量下载

使用 selenium 自动化工具模拟用户下载。

**注意：本项目不提供任何数据库下载账号，需要使用者自行准备。代码开源，保证不会窃取账号信息。**

浏览器目前支持：[Google Chrome](https://www.google.com/chrome/)

数据库目前支持：[知网](https://www.cnki.net/)、[万方](https://www.wanfangdata.com.cn/)

## 使用方法

### 可执行文件（推荐）

1. 前往 [release](https://github.com/jklincn/PaperDownloader/releases) 页面下载最新可执行文件，双击运行。
2. 在可选浏览器中选择一个浏览器打开。
3. 点击【获取 WebDriver】按钮，自动下载打开浏览器所对应的 WebDriver。**如果后续没有选择其他浏览器或者升级当前浏览器版本，则只需第一次使用时获取。**
4. 在浏览器中打开相应数据库网站，登陆并检索所需内容，在需要下载的论文前面打上勾。
5. 点击界面右侧【下载】按钮，开始自动模拟下载，等待下载结束。

### 运行源代码

1. 下载本项目代码，有以下两种方法：

   - 使用 Git 克隆项目

     ```
     git clone https://github.com/jklincn/PaperDownloader.git
     ```

   - 在 GitHub 界面选择 Download ZIP，再解压

2. 在 PaperDownloader 文件夹中打开终端，执行

   ```
   pip install -r requirements.txt
   python gui.py
   ```

3. 后续使用方法同上步骤【2-5】。

## 演示视频

## 参数设置

**默认情况下无需改动**。点击界面右侧【设置】按钮，即可打开设置面板。

目前支持设置的参数有：

- Google Chrome 可执行文件路径
- 下载间隔时间

## 未来工作

未来工作取决于大家的需求反馈，可以通过 issue 或者 email 来提出需求。

- [ ] 支持多种浏览器（Microsoft Edge、Mozilla Firefox等）
- [ ] 支持多类数据库（**万方（已支持）**、维普等）
- [x] 方便使用的图形用户界面
- [ ] 支持使用默认用户数据文件（这样可以使用原已保存在浏览器中的账号密码，快速登录知网）
- [x] 更完善的操作错误检查提示
- [ ] 支持 CAJ 下载（当 PDF 不可用时）
- [x] 自动下载对应浏览器版本的 WebDriver
- [ ] 代码结构优化完善

## 已知问题

1. 问题：如果下载间隔过小，短时间下载次数过多，有可能引发知网反爬机制（需要输入验证码或者拖动图形等）。

   解决方法：增加下载间隔时间，分散下载操作。

2. 问题：使用脚本后，有可能会在桌面创建 Google Chrome 的快捷方式。

   解决方法：浏览器默认设置问题，暂未解决。目前需要手动删除。

## 联系方式

E-mail：jklincn@outlook.com

