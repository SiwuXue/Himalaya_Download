# 喜马拉雅音频下载器

一个基于 Python 的桌面应用，支持批量下载喜马拉雅专辑音频，界面美观，操作简单。

## 主要功能
- 支持专辑/声音ID搜索与批量下载
- 支持多线程下载，显示实时下载进度
- 支持MP3/M4A格式切换
- 支持自动/手动获取Cookie
- 下载目录自定义
- 现代化美观界面

## 环境依赖
- Python 3.7 及以上
- 依赖库：
  - tkinter
  - requests
  - selenium
  - tqdm（如有进度条需求）
  - 其他依赖见 requirements.txt

## 运行方法
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行主程序：
   ```bash
   python Graph/download.py
   ```

## 打包为桌面应用（exe）
1. 安装 PyInstaller：
   ```bash
   pip install pyinstaller
   ```
2. 打包命令（假设主程序为 download.py，图标为 logo.ico）：
   ```bash
   pyinstaller --noconsole --onefile --icon=logo.ico Graph/download.py
   ```
3. 打包后在 dist 目录下找到 exe 文件。

## 常见问题
- **界面卡死/无响应？**
  - 请勿在主线程 join 线程，下载任务应在后台线程执行。
- **图标不显示？**
  - 请确保 logo.ico 为标准 ICO 格式，且路径正确。
- **依赖缺失？**
  - 请检查 requirements.txt 并重新安装依赖。

## 联系方式
- 作者：无忧
- 微信：yie6690g
- 仅供学习交流，禁止商业用途。 
