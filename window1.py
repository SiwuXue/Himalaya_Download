import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.ttk import *
import subprocess
from tkinter import messagebox
from search import Search 
from download import Download
import os


class Window1:
    def __init__(self, parent):
        self.window = parent
        self.window.title("喜马拉雅音频下载")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        self.window.config(bg="#eaf6fb")
        try:
            ico_path = os.path.abspath("logo.ico")
            self.window.iconbitmap(ico_path)
        except Exception as e:
            print("图标设置失败：", e)
        self.create_widgets()

    def create_widgets(self):
        self.creat_menbar()
        self.font_toolbar_frame = tk.Frame(self.window, relief=tk.RAISED, bd=1, bg="lightgray")
        self.font_toolbar_frame.pack_forget()  # 初始隐藏
        self.write_text()
        # self.creat_scrollbar()

    def creat_scrollbar(self):
        # 创建Y滚动条
        self.yscrollbar = tk.Scrollbar(self.window)
        self.yscrollbar.pack(side=tk.LEFT, fill=tk.Y)  # 让滚动条在左侧垂直方向上填充窗口
        self.yscrollbar.config(command=self.text.yview)  # 配置滚动条与Text组件的关联
        self.text.config(yscrollcommand=self.yscrollbar.set)  # 配置Text组件与滚动条的关联
        # 创建X滚动条
        self.xscrollbar = tk.Scrollbar(self.window, orient=tk.HORIZONTAL)  # 创建水平方向的滚动条
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)  # 让滚动条在底部水平方向上填充窗口
        self.xscrollbar.config(command=self.text.xview)  # 配置滚动条与Text组件的关联
        self.text.config(xscrollcommand=self.xscrollbar.set)  # 配置Text组件与滚动条的关联
    def creat_menbar(self):
        # 创建菜单栏
        self.menubar = tk.Menu(self.window)
        # 创建文件菜单
        self.filemenu = tk.Menu(self.menubar, tearoff=1)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="搜索", command=lambda: Search(tk.Toplevel(self.window)))  # 修改为打开搜索窗口
        self.filemenu.add_command(label="下载", command=lambda: Download(tk.Toplevel(self.window)))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="退出", command=self.window.destroy)

        # 创建设置菜单
        self.settingmenu = tk.Menu(self.menubar, tearoff=1)
        self.menubar.add_cascade(label="Setting", menu=self.settingmenu)
        self.settingmenu.add_command(label="Font", command=self.toggle_font_toolbar)
        self.settingmenu.add_command(label="Theme", command=self.toggle_color_scale)  # 修改为切换功能
        # 创建帮助菜单
        self.helpmenu = tk.Menu(self.menubar, tearoff=1)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About me", command=self.about_me)

        self.window.config(menu=self.menubar)    
    def show_font_toolbar(self):
        # 显示工具栏并置于文本上方
        self.font_toolbar_frame.pack(fill=tk.X, padx=2, pady=(2,0), before=self.text)

    def font_toolbar_init(self):
        # 只初始化一次
        if hasattr(self, 'font_toolbar_inited') and self.font_toolbar_inited:
            return
        self.font_toolbar_inited = True

        # 背景色和边框
        self.font_toolbar_frame.config(bg="#f5f5f5", bd=2, relief="groove", padx=10, pady=5)

        # 字体
        tk.Label(self.font_toolbar_frame, text="字体：", font=("微软雅黑", 10), bg="#f5f5f5").pack(side=tk.LEFT, padx=(0,2))
        self.familyVar = tk.StringVar()
        self.familyFamily = ("Arial", "Times New Roman", "Verdana", "Courier New", "SimSun", "SimHei", "KaiTi")
        self.familyVar.set(self.familyFamily[0])
        self.fontChange = FontChange(self)
        family_menu = ttk.OptionMenu(self.font_toolbar_frame, self.familyVar, self.familyFamily[0], *self.familyFamily, command=self.fontChange.familyChange)
        family_menu.pack(side=tk.LEFT, padx=(0,10))

        # 字号
        tk.Label(self.font_toolbar_frame, text="字号：", font=("微软雅黑", 10), bg="#f5f5f5").pack(side=tk.LEFT, padx=(0,2))
        self.sizeVar = tk.IntVar()
        self.sizeVar.set(12)
        size_menu = ttk.OptionMenu(self.font_toolbar_frame, self.sizeVar, 12, *range(8, 24), command=self.fontChange.sizeSelected)
        size_menu.pack(side=tk.LEFT, padx=(0,10))

        # 粗细
        tk.Label(self.font_toolbar_frame, text="粗细：", font=("微软雅黑", 10), bg="#f5f5f5").pack(side=tk.LEFT, padx=(0,2))
        self.weightVar = tk.StringVar()
        self.weightFamily = ("normal", "bold")
        self.weightVar.set(self.weightFamily[0])
        weight_menu = ttk.OptionMenu(self.font_toolbar_frame, self.weightVar, self.weightFamily[0], *self.weightFamily, command=self.fontChange.weightChange)
        weight_menu.pack(side=tk.LEFT, padx=(0,10))

    def write_text(self):
        self.text = tk.Text(self.window, bg="#eaf6fb", font=("微软雅黑", 12), relief="flat", bd=0)
        self.text.pack(fill=tk.BOTH, expand=True, pady=(50, 5), padx=30)
        self.text.insert(tk.END, "欢迎你来到喜马拉雅音频下载程序，更多功能正在开发中，欢迎加微信一起讨论。")
        self.font_toolbar_init()

    def on_resize(self, event):
        frame_width = self.function_frame.winfo_width()
        padding = max((frame_width - btn_width) // 2, 10)
        for btn in [self.btn1, self.btn2, self.btn3, self.btn4]:
            btn.pack_configure(padx=padding)
    
    def about_me(self, event=None):
        messagebox.showinfo("About me", "本软件仅供内部交流，不得用于商业用途。\n本软件由Python3开发，使用tkinter库。\n软件作者：王伟\n微信：yie6690g")
    
    def toggle_color_scale(self):
        """切换颜色滑块的显示状态"""
        if hasattr(self, 'color_frame') and self.color_frame.winfo_ismapped():
            self.color_frame.pack_forget()  # 隐藏
        else:
            self.create_color_scale()  # 只会创建一次，后续只是显示

    def create_color_scale(self):
        """美化后的颜色调节滑块，只创建一次"""
        if hasattr(self, 'color_frame') and self.color_frame.winfo_exists():
            self.color_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
            return

        from tkinter import ttk

        self.color_frame = tk.Frame(self.window, bg="#f5f5f5", bd=2, relief="groove")
        self.color_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=30, pady=20)

        # 标题
        title = tk.Label(self.color_frame, text="主题颜色调节", font=("微软雅黑", 12, "bold"), bg="#f5f5f5")
        title.grid(row=0, column=0, columnspan=3, pady=(5, 10))

        # 红色
        tk.Label(self.color_frame, text="红色:", font=("微软雅黑", 10), bg="#f5f5f5").grid(row=1, column=0, sticky="e", padx=(10, 2))
        self.red_scale = ttk.Scale(self.color_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=180, command=self.update_bg_color)
        self.red_scale.set(0)
        self.red_scale.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        self.red_value = tk.Label(self.color_frame, text="0", width=3, bg="#f5f5f5")
        self.red_value.grid(row=1, column=2, sticky="w")

        # 绿色
        tk.Label(self.color_frame, text="绿色:", font=("微软雅黑", 10), bg="#f5f5f5").grid(row=2, column=0, sticky="e", padx=(10, 2))
        self.green_scale = ttk.Scale(self.color_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=180, command=self.update_bg_color)
        self.green_scale.set(0)
        self.green_scale.grid(row=2, column=1, padx=5, pady=5, sticky="we")
        self.green_value = tk.Label(self.color_frame, text="0", width=3, bg="#f5f5f5")
        self.green_value.grid(row=2, column=2, sticky="w")

        # 蓝色
        tk.Label(self.color_frame, text="蓝色:", font=("微软雅黑", 10), bg="#f5f5f5").grid(row=3, column=0, sticky="e", padx=(10, 2))
        self.blue_scale = ttk.Scale(self.color_frame, from_=0, to=255, orient=tk.HORIZONTAL, length=180, command=self.update_bg_color)
        self.blue_scale.set(0)
        self.blue_scale.grid(row=3, column=1, padx=5, pady=5, sticky="we")
        self.blue_value = tk.Label(self.color_frame, text="0", width=3, bg="#f5f5f5")
        self.blue_value.grid(row=3, column=2, sticky="w")

        # 让滑块随窗口宽度自适应
        self.color_frame.columnconfigure(1, weight=1)

    def update_bg_color(self, _=None):
        # 检查滑块是否存在
        if not (hasattr(self, 'red_scale') and hasattr(self, 'green_scale') and hasattr(self, 'blue_scale')):
            return
        if not (hasattr(self, 'red_value') and hasattr(self, 'green_value') and hasattr(self, 'blue_value')):
            return
        r = int(self.red_scale.get())
        g = int(self.green_scale.get())
        b = int(self.blue_scale.get())
        self.red_value.config(text=str(r))
        self.green_value.config(text=str(g))
        self.blue_value.config(text=str(b))
        color = f"#{r:02x}{g:02x}{b:02x}"
        self.window.config(bg=color)

    def toggle_font_toolbar(self):
        """切换字体工具栏的显示状态"""
        if self.font_toolbar_frame.winfo_ismapped():
            self.font_toolbar_frame.pack_forget()
        else:
            self.font_toolbar_frame.pack(fill=tk.X, padx=20, pady=(10,0), before=self.text)

class FontChange:
    def __init__(self, window):
        self.window = window

    def familyChange(self, event):
        # 改变字体
        f1 = tkfont.Font(family=self.window.familyVar.get())
        self.window.text.configure(font=f1)

    def sizeSelected(self, event):
        # 改变字号
        f2 = tkfont.Font(size=self.window.sizeVar.get())
        self.window.text.configure(font=f2)

    def weightChange(self, event):
        # 改变粗细
        f3 = tkfont.Font(weight=self.window.weightVar.get())
        self.window.text.configure(font=f3)

if __name__ == "__main__":
    root = tk.Tk()
    app = Window1(root)
    root.mainloop()