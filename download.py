import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import threading
import os

class Download:
    def __init__(self, root):
        self.root = root
        self.root.title("音频下载")
        self.root.geometry("950x650")
        self.root.configure(bg="#eaf6fb")  # 柔和浅蓝
        
        # 设置中文字体
        self.font = ('SimHei', 10)

        
        
        # 初始化默认下载目录（使用用户主目录的Downloads文件夹）
        import os
        default_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        # 检查目录是否存在，不存在则使用用户主目录
        self.download_dir = default_dir if os.path.isdir(default_dir) else os.path.expanduser('~')
        
        # 创建搜索框和按钮
        self.create_function_frame()
        # 创建表格视图
        self.create_table_view()
        # 初始化进度条
        # self.ProgessBar = ProgressBar(self.root)
        # self.ProgessBar.progress_values = {}
        # self.ProgessBar.create_progressbar_style()
        # 获取最大页数
        self.get_pageId()

    def get_pageId(self):
        """获取最大页数"""
        self.headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                    "Host": "www.ximalaya.com",
                    "cookies": "_xmLog=h5&68d3d856-aa91-4acf-acdb-cc53824e1517&process.env.sdkVersion; wfp=ACNjODU0ODIzZTNiZGE5NGEzg---1WMvj0J4bXdlYl93d3c; 1&remember_me=y; 1&_token=535280106&4D163180340NE43C725EB42DD5D927D26FFCB2B5C7FAA1593F6E472BB4AE3E740E3BCF13F67C161MEF9606658CD57E4_; HWWAFSESID=8e832c424508c44397; HWWAFSESTIME=1747312825603; DATE=1746547298613; crystal=U2FsdGVkX1+1Z92npdPBD5j6SFhEqEvUbgCC+MHxGo7BOLzRQNgqHXN1+Qv+jXKj/gsTv5AxEP/of7fsQTaaps8OKgn2VqlRhRmpmZK94Ct1b8yB7/anvZ1w/GnSbOP/kbhnfj5X+4xscR3NoHWylUO4j96IiH90c9GjnepBV5v4pZtH9tEOcCeHnCRqgxR+7wZYMiR/eOMIoKKqGFtBnqpyj2CW4ph8qULp4f1ghWOEjgVui1nNgOtGFtiugjXF; xm-page-viewid=ximalaya-web; impl=www.ximalaya.com.login; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1746547302,1746548230,1746714778,1747312830; HMACCOUNT=A06853B63764C5EA; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1747318263; cmci9xde=U2FsdGVkX1+RFZr3xXt5PuBkVqQm1VHHIyHs7jb/+YNO0+QSbtYfw/KDjmeRTKjGxqI8qpAfA83oBlzwrwBEQg==; pmck9xge=U2FsdGVkX19czV4ebIp9P3ROQrRdSu9z76B/L+ROvfc=; assva6=U2FsdGVkX1+X07TMTnfUfEEPX18CBu9twg7vYY1IoNc=; assva5=U2FsdGVkX187iblLMQxlvLVlLTDgTl+sV8PjfUWCzygEtkXABxwUia+7oUZ5iFeX9X0bnup1vZLddoMOHFvSiw==; vmce9xdq=U2FsdGVkX1+wvya4rfVA40Cb22Bebi0rttrGFy8yAa6QPh4WTC4IMVG44jcGa1pO6ZQs5iGqivnvqfztb+n1lJVKcf6BEc3t4WJNAjrbMss+Swm1XujuUfVX/6D8EaQL6dRE3w+L+zpsUXqtCqb03yUIkAQPUhDRD4BgenAIzmE=; web_login=1747322100285"
                }
        keyword = self.id_entry.get().strip()
        if not keyword:
            messagebox.showwarning("警告", "请输入搜索专辑ID")
            return
        
        # 清空表格
        for item in self.table.get_children():
            self.table.delete(item)
        base_url = f"http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId={keyword}&pageId=1"
        res = requests.get(url = base_url,headers=self.headers)
        res.encoding = "utf-8" 
        res_dict = res.json()
        maxPageId = res_dict["maxPageId"]   # 页数
        self.maxPageId = maxPageId  # 保存最大页数到类变量   

    def adjust_entry_width(self, event=None):
        """动态调整Entry宽度以适应文本内容"""
        text = self.file_entry.get()
        # 计算文本长度（假设中/英文字符宽度一致）
        text_length = len(text)
        # 设置最小/最大宽度（根据实际需求调整）
        min_width = 15  # 最小宽度（初始值）
        max_width = 40  # 最大宽度（防止过宽）
        # 计算新宽度（文本长度+2用于左右留白）
        new_width = max(min_width, min(text_length + 2, max_width))
        self.file_entry.config(width=new_width)

    def on_entry_return(self, event=None):
        """处理Entry中按回车键创建路径并检测"""
        import os
        path = self.file_entry.get().strip()
        if not path:
            messagebox.showwarning("提示", "路径不能为空")
            return
        
        if os.path.exists(path):
            messagebox.showinfo("提示", f"路径已存在：{path}")
            return
        
        try:
            os.makedirs(path, exist_ok=True)  # exist_ok=True避免路径已存在时报错
            messagebox.showinfo("成功", f"路径创建成功：{path}")
            # 更新类变量保存当前路径
            self.download_dir = path
        except Exception as e:
            messagebox.showerror("错误", f"创建路径失败：{str(e)}")

    def create_function_frame(self):
        """创建功能框（修改部分）"""
        main_frame = ttk.Frame(self.root, padding=20, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 第一列
        list1_frame = ttk.Frame(main_frame)
        list1_frame.pack(side = tk.LEFT,fill=tk.Y)

        ttk.Separator(list1_frame, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y, pady=(30,2))
        # 第一列第一行
        list1_row1_frame = ttk.Frame(list1_frame)
        list1_row1_frame.pack(fill=tk.X, pady=5)
        ttk.Label(list1_row1_frame, text="ID:").pack(side=tk.LEFT, padx=8, pady=8)
        self.id_entry = ttk.Entry(list1_row1_frame, width=12)
        self.id_entry.pack(side=tk.LEFT, padx=8, pady=8)
        search_btn = ttk.Button(list1_row1_frame, text="解析", style="Accent.TButton", command=self.fetch_and_display_data)
        search_btn.pack(side=tk.LEFT, padx=8, pady=8)

        # 第一列第二行
        list1_row2_frame = ttk.Frame(list1_frame)
        list1_row2_frame.pack(fill=tk.X)
        self.search_type = tk.StringVar(value="album")
        ttk.Radiobutton(list1_row2_frame, text="专辑", variable=self.search_type, 
                       value="album").pack(side = tk.LEFT,fill=tk.X, padx=5)
        ttk.Radiobutton(list1_row2_frame, text="声音 ", variable=self.search_type,
                       value="track").pack(side = tk.LEFT,fill=tk.X, padx=5)

        # 第一列第三行，MP3/M4A选择
        list1_row3_frame = ttk.Frame(list1_frame)
        list1_row3_frame.pack(fill=tk.X)
        self.download_type = tk.StringVar(value="mp3")
        ttk.Radiobutton(list1_row3_frame, text="MP3", variable=self.download_type,
                       value="mp3").pack(side=tk.LEFT,fill=tk.X, padx=5)
        ttk.Radiobutton(list1_row3_frame, text="M4A", variable=self.download_type,
                       value="flac").pack(side=tk.LEFT,fill=tk.X, padx=5)




        # 第一行（修改部分）
        # 创建样式配置背景色
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#eaf6fb')
        style.configure('Card.TFrame', background='#fff', relief='groove', borderwidth=2)
        style.configure('Accent.TButton', font=('微软雅黑', 11), foreground='#fff', background='#4CAF50', padding=6)
        style.configure('TLabel', font=('微软雅黑', 11), background='#fff')
        style.configure('TEntry', font=('微软雅黑', 11))
        style.configure('TSpinbox', font=('微软雅黑', 11))
        style.configure('Treeview.Heading', font=('微软雅黑', 11, 'bold'))
        style.configure('Treeview', font=('微软雅黑', 10), rowheight=28)
        style.map('Accent.TButton', background=[('active', '#388e3c')])
        row1_frame = ttk.Frame(main_frame, style='Red.TFrame')  # 应用样式
        row1_frame.pack(fill=tk.X, pady=0)
               
        select_dir_btn = ttk.Button(row1_frame, text="选择目录", 
                                  command=self.select_directory)
        select_dir_btn.pack(side=tk.LEFT, padx=5)
        # 选择目录后的文件路径输入框
        self.file_entry = ttk.Entry(row1_frame, width=50, font=self.font)
        self.file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        # 初始化时填充默认路径
        self.file_entry.insert(0, self.download_dir)
        # 绑定键盘释放事件（输入/删除时触发）
        self.file_entry.bind("<KeyRelease>", self.adjust_entry_width)
        # 绑定回车键事件（新增）
        self.file_entry.bind("<Return>", self.on_entry_return)
        # 初始化时调整宽度（适应初始文本）
        self.adjust_entry_width()

        # 第二行
        row2_frame = ttk.Frame(main_frame)
        row2_frame.pack(fill=tk.X)
        
 

        # 修改Cookie获取方式下拉菜单
        self.cookie_method = tk.StringVar(value="auto")
        cookie_menu = ttk.OptionMenu(row2_frame, self.cookie_method, "自动获取Cookie", 
                                   *["自动获取Cookie", "手动输入Cookie"],
                                   command=self.handle_cookie_method_change)
        cookie_menu.pack(side=tk.LEFT, padx=5)


        # 第三行
        row3_frame = ttk.Frame(main_frame)
        row3_frame.pack(fill=tk.X)
        


        # 线程数
        self.thread_num = tk.IntVar(value=1)
        ttk.Label(row3_frame, text="线程:", font=self.font).pack(side=tk.LEFT, padx=(5,0))
        ttk.Spinbox(row3_frame, from_=1, to=10, textvariable=self.thread_num,
                   width=3).pack(side=tk.LEFT, padx=(0,5))

        # 添加样式
        style = ttk.Style()
        style.configure('Accent.TButton', font=self.font)
        style.configure('Accent.TProgressbar', troughcolor='#eaf6fb', background='#4CAF50', thickness=18)  # 添加进度条样式

        # 进度条
        # self.progress_var = tk.DoubleVar()
        # progress_bar = ttk.Progressbar(row3_frame, variable=self.progress_var,
        #                              maximum=100, style='Accent.TProgressbar')
        # progress_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # 下载按钮
        download_btn = ttk.Button(row3_frame, text="下载", command=self.start_download)
        download_btn.pack(side=tk.LEFT, padx=5)
 
        # 添加样式
        style = ttk.Style()
        style.configure('Accent.TButton', font=self.font)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

    def create_table_view(self):
        """创建表格视图"""
        table_frame = ttk.Frame(self.root, padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Treeview表格
        columns = ("序号", "标题", "ID", "下载进度")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")
        
        # 设置列标题
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center")
        self.table.pack(fill=tk.BOTH, expand=True)
        
        # 添加右键菜单
        self.table.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="复制", command=self.copy_selected)

    def show_context_menu(self, event):
        """显示右键菜单"""
        item = self.table.identify_row(event.y)
        if item:
            self.context_menu.post(event.x_root, event.y_root)

    def copy_selected(self):
        """复制选中内容"""
        selected_item = self.table.focus()
        if selected_item:
            item_data = self.table.item(selected_item)['values']
            text_to_copy = "\t".join(str(x) for x in item_data)
            self.root.clipboard_clear()
            self.root.clipboard_append(text_to_copy)

    def fetch_and_display_data(self):
        """获取数据并在表格中显示"""
        keyword = self.id_entry.get().strip()
        if not keyword:
            messagebox.showwarning("警告", "请输入搜索专辑ID")
            return

        # 检查maxPageId
        if not hasattr(self, "maxPageId") or self.maxPageId is None:
            self.get_pageId()
            if not hasattr(self, "maxPageId") or self.maxPageId is None:
                messagebox.showwarning("警告", "请先输入专辑ID并点击解析")
                return

        # 清空表格
        for item in self.table.get_children():
            self.table.delete(item)
        
        # 初始化全局计数器
        global_index = 1
        
        for i in range(1,self.maxPageId+1):
              
            try:
                # 构建请求URL
                url = f"http://mobwsa.ximalaya.com/mobile/playlist/album/page?albumId={keyword}&pageId={i}"

                # 获取数据
                res = requests.get(url, headers=self.headers)
                res.encoding = "utf-8" 
                res_dict = res.json()
                res.raise_for_status()  # 检查请求是否成功
                data = res_dict["list"]
                # 在表格中显示数据
                self.display_data_in_table(data, global_index)
                # 更新全局计数器
                global_index += len(data)
                
            except requests.exceptions.RequestException as e:
                messagebox.showerror("错误", f"请求失败: {str(e)}")
            except json.JSONDecodeError:
                messagebox.showerror("错误", "无法解析JSON数据，请确认API返回的是有效的JSON格式")
            except Exception as e:
                messagebox.showerror("错误", f"发生未知错误: {str(e)}")

    def display_data_in_table(self, data, start_index=1):
        """在表格中显示数据"""
        # 假设JSON数据是一个列表，每个元素是一个字典
        if not isinstance(data, list):
            messagebox.showwarning("警告", "JSON数据不是预期的列表格式")
            return
        
        if not data:
            messagebox.showinfo("提示", "没有找到相关数据")
            return
        
        # 遍历数据并添加到表格中，使用传入的起始索引
        current_index = start_index
        for item in data:
            title = item["title"]
            ID = item["trackId"]
            mp3 = item.get("playUrl64", "")
            m4a = item.get("playPathAacv224", "")
            self.table.insert("", "end", values=(current_index, title, ID, "", mp3, m4a))
            current_index += 1

    def getCookies():
        # 使用selenium自动获取cookies
        chrome_options = Options()
        # 设置浏览器参数
        # --headless：无头浏览器，不显示浏览器窗口
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.ximalaya.com/')
        time.sleep(5)  # 等待页面加载完成，这里可以根据实际情况调整等待时间
        cookie = driver.get_cookies()
        driver.quit()
        # cookies格式化
        # print(cookie)
        cookie_dict = {item["name"]: item["value"] for item in cookie}
        return cookie_dict  # 返回格式化后的cooki   



    def handle_cookie_method_change(self, method):
        """处理Cookie获取方式变更"""
        if method == "自动获取Cookie":
            try:
                self.cookies = self.getCookies()  # 保存到类变量
                messagebox.showinfo("提示", "Cookie已自动获取")
            except Exception as e:
                messagebox.showerror("错误", f"自动获取Cookie失败: {str(e)}")
        else:
            # 创建手动输入对话框
            input_dialog = tk.Toplevel(self.root)
            input_dialog.title("手动输入Cookie")
            input_dialog.geometry("400x180")
            input_dialog.resizable(False, False)
            input_dialog.configure(bg="#f5f5f5")
            # 居中
            input_dialog.update_idletasks()
            x = (input_dialog.winfo_screenwidth() - 400) // 2
            y = (input_dialog.winfo_screenheight() - 180) // 2
            input_dialog.geometry(f"+{x}+{y}")

            # 标题
            title_label = tk.Label(input_dialog, text="请输入Cookie", font=("微软雅黑", 12, "bold"), bg="#f5f5f5")
            title_label.pack(pady=(18, 8))

            # 输入框
            entry_frame = tk.Frame(input_dialog, bg="#f5f5f5")
            entry_frame.pack(pady=(0, 10))
            cookie_entry = tk.Entry(entry_frame, width=38, font=("微软雅黑", 10), relief="groove", bd=2)
            cookie_entry.pack(ipady=4)

            # 按钮
            btn_style = ttk.Style()
            btn_style.configure("Accent.TButton", font=("微软雅黑", 10), foreground="#fff", background="#4CAF50")
            confirm_btn = ttk.Button(input_dialog, text="确认", style="Accent.TButton",
                                     command=lambda: self.save_manual_cookie(cookie_entry.get(), input_dialog))
            confirm_btn.pack(pady=(0, 10))

            # 让输入框自动获得焦点
            cookie_entry.focus_set()

    def save_manual_cookie(self, cookie, dialog):
        # 保存手动输入的Cookie
        if cookie:
            # 这里可以添加Cookie验证逻辑
            messagebox.showinfo("提示", "Cookie已保存")
            dialog.destroy()
        else:
            messagebox.showwarning("警告", "Cookie不能为空")

    def getCookies(self):
        # 使用selenium自动获取Cookies
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get('https://www.ximalaya.com/')
            time.sleep(5)
            cookies = driver.get_cookies()
            driver.quit()
            
            # 转换为requests可用的格式
            cookie_dict = {item["name"]: item["value"] for item in cookies}
            return cookie_dict
        except Exception as e:
            raise Exception(f"获取Cookie时出错: {str(e)}")
    def select_directory(self):
        """打开目录选择对话框并同步到Entry（调整窗口大小）"""
        from tkinter import filedialog
        # 指定父窗口为当前主窗口，并设置对话框标题（可选）
        dir_path = filedialog.askdirectory(
            parent=self.root,  # 指定父窗口，对话框会基于父窗口尺寸自适应
            title="选择下载目录"  # 设置对话框标题（可选优化）
        )
        if dir_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, dir_path)
            messagebox.showinfo("选择目录", f"已选择目录: {dir_path}")
            self.download_dir = dir_path

    def start_download(self):
        download_type = self.download_type.get()
        items = self.table.get_children()
        download_list = []
        for item in items:
            values = self.table.item(item)['values']
            seq, title, track_id, _, mp3, m4a = values
            url = mp3 if download_type == "mp3" else m4a
            download_list.append((seq, title, track_id, url, item))
        if not download_list:
            messagebox.showwarning("警告", "没有可下载的音频")
            return

        def chunks(lst, n):
            avg = len(lst) // n
            rem = len(lst) % n
            result = []
            start = 0
            for i in range(n):
                end = start + avg + (1 if i < rem else 0)
                result.append(lst[start:end])
                start = end
            return [chunk for chunk in result if chunk]

        thread_count = self.thread_num.get()
        chunked = chunks(download_list, thread_count)
        threads = []
        for chunk in chunked:
            t = threading.Thread(target=self.download_tracks, args=(chunk,))
            threads.append(t)
            t.start()

        # 用后台线程监控所有下载线程
        def wait_for_all():
            for t in threads:
                t.join()
            self.root.after(0, lambda: messagebox.showinfo("完成", "所有下载任务已完成！"))

        threading.Thread(target=wait_for_all, daemon=True).start()

    def download_tracks(self, track_info_list):
        for seq, title, track_id, url, item_id in track_info_list:
            if not url:
                self.table.after(0, self.table.set, item_id, "下载进度", "无下载链接")
                continue
            try:
                # 文件名处理
                ext = os.path.splitext(url)[-1] or ".mp3"
                safe_title = "".join(c if c not in r'\/:*?"<>|' else "_" for c in str(title))
                local_filename = os.path.join(self.download_dir, f"{safe_title}_{track_id}{ext}")
                with requests.get(url, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    total = int(r.headers.get('content-length', 0))
                    downloaded = 0
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                percent = int(downloaded * 100 / total) if total else 0
                                # 线程安全更新进度
                                self.table.after(0, self.table.set, item_id, "下载进度", f"{percent}%")
                self.table.after(0, self.table.set, item_id, "下载进度", "完成")
            except Exception as e:
                self.table.after(0, self.table.set, item_id, "下载进度", f"失败:{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Download(root)
    root.mainloop()