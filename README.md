# 知网数据库批量下载

使用 selenium 自动化工具模拟用户下载。

**注意：本脚本不提供知网数据库下载账号，需要使用者自行准备。**

## 前提条件

- 使用 Google Chrome 浏览器
- 具备执行 python 代码的环境，包括 pip

## 使用方法

1. 下载本项目代码，有以下两种方法：

   - 使用 Git 克隆项目

     ```
     git clone https://github.com/jklincn/PaperDownloader.git
     ```

   - 在 GitHub 界面选择 Download ZIP，再解压

2. 安装依赖

   ```
   pip install selenium==4.11.2
   ```

3. 使用 prepare 参数运行脚本，将自动打开浏览器，登录知网后进行所需内容的检索，**在需要下载的论文前面打上勾**。

   ```
   python run.py prepare
   ```

4. 使用 download 参数运行脚本，即可开始下载，期间不要对浏览器进行操作。

   ```
   python run.py download
   ```

   所有下载完成后，终端会输出以下字样：

   ```
   Download completed, total number of papers: 20（根据实际情况变化）
   ```

## 参数配置

**默认情况下无需改动**

- ChromePath：Google Chrome 可执行文件路径。默认："C:\Program Files\Google\Chrome\Application\chrome.exe"。如果不是默认安装路径，则需要手动更改。
- Interval：下载间隔时间，单位为秒。默认：3。
- TempUserDateDir：临时用户数据存放目录。默认：当前目录下的 chrome_temp_data。如果不存在则会自动创建。可以使用 python run.py clean 清理目录。

## 兼容性测试

| 测试时间   | 浏览器版本                  | 测试操作                |
| ---------- | --------------------------- | ----------------------- |
| 2023-08-16 | Google Chrome 116.0.5845.97 | 知网间隔3秒批量下载20篇 |

## 未来工作

未来工作取决于大家的需求反馈，可以通过 issue 或者 email 来提出需求。

- [ ] 支持多种浏览器（Microsoft Edge、Mozilla Firefox等）
- [ ] 支持多类数据库（万方、维普等）
- [ ] 方便使用的图形用户界面
- [ ] 支持使用默认用户数据文件（这样可以使用原已保存在浏览器中的账号密码，快速登录知网）
- [ ] 更完善的操作错误检查提示
- [ ] 支持 CAJ 下载（当 PDF 不可用时）

## 已知问题

1. 问题：如果下载间隔过小，短时间下载次数过多，有可能引发知网反爬机制（需要输入验证码或者拖动图形等）。

   解决方法：增加间隔时间，分散下载操作。

2. 问题：使用脚本后，有可能会在桌面创建 Google Chrome 的快捷方式。

   解决方法：暂未查明创建原因，删除即可。

## 联系方式

E-mail：jklincn@outlook.com

