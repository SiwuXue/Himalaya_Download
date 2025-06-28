import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

class Search:
    def __init__(self, root):
        self.root = root
        self.root.title("Search")
        self.root.geometry("900x600")
        
        # 设置中文字体
        self.font = ('SimHei', 10)
        
        # API基础URL
        self.base_url = 'https://www.ximalaya.com/revision/search?core=album&kw='
        
        # 创建搜索框和按钮
        self.create_search_frame()
        
        # 创建表格视图
        self.create_table_view()

    def create_search_frame(self):
        """创建搜索框和按钮的框架"""
        search_frame = ttk.Frame(self.root, padding="10")
        search_frame.pack(fill=tk.X)
        
        # 第一行：搜索框和按钮
        row1_frame = ttk.Frame(search_frame)
        row1_frame.pack(fill=tk.X)
        
        ttk.Label(row1_frame, text="请输入搜索专辑:", font=self.font).pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(row1_frame, width=50, font=self.font)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.insert(0, "斗罗大陆")
        
        search_btn = ttk.Button(row1_frame, text="搜索", command=self.fetch_and_display_data,
                              style='Accent.TButton')
        search_btn.pack(side=tk.LEFT, padx=5)

        # 第二行：复选框
        row2_frame = ttk.Frame(search_frame)
        row2_frame.pack(fill=tk.X)
        
        self.include_vip = tk.BooleanVar()
        vip_checkbox = ttk.Checkbutton(row2_frame, text="包含VIP", variable=self.include_vip,
                                      style='Accent.TCheckbutton')
        vip_checkbox.pack(side=tk.LEFT, padx=(5,2))
        # 添加样式
        style = ttk.Style()
        style.configure('Accent.TButton', font=self.font)

    def create_table_view(self):
        """创建表格视图"""
        table_frame = ttk.Frame(self.root, padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Treeview表格
        columns = ("序号", "标题", "作者", "分类", "ID", "vip(0免费2会员)")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # 设置列标题
        for col in columns:
            self.table.heading(col, text=col)
            # 根据列名设置列宽
            if col == "标题":
                self.table.column(col, width=300)
            elif col == "作者":
                self.table.column(col, width=120)
            elif col == "分类":
                self.table.column(col, width=80)
            elif col == "ID":
                self.table.column(col, width=80)
            elif col == "vip":
                self.table.column(col, width=160)
            else:
                self.table.column(col, width=20)
        
        # 添加滚动条
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)
        
        # 布局
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
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
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("警告", "请输入搜索专辑")
            return
        
        # 清空表格
        for item in self.table.get_children():
            self.table.delete(item)
        
        try:
            # 构建完整URL
            url = self.base_url + keyword
            headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Host": "www.ximalaya.com",
        "cookies": 
    "_xmLog=h5&68d3d856-aa91-4acf-acdb-cc53824e1517&process.env.sdkVersion; wfp=ACNjODU0ODIzZTNiZGE5NGEzg---1WMvj0J4bXdlYl93d3c; 1&remember_me=y; 1&_token=535280106&4D163180340NE43C725EB42DD5D927D26FFCB2B5C7FAA1593F6E472BB4AE3E740E3BCF13F67C161MEF9606658CD57E4_; HWWAFSESID=8e832c424508c44397; HWWAFSESTIME=1747312825603; DATE=1746547298613; crystal=U2FsdGVkX1+1Z92npdPBD5j6SFhEqEvUbgCC+MHxGo7BOLzRQNgqHXN1+Qv+jXKj/gsTv5AxEP/of7fsQTaaps8OKgn2VqlRhRmpmZK94Ct1b8yB7/anvZ1w/GnSbOP/kbhnfj5X+4xscR3NoHWylUO4j96IiH90c9GjnepBV5v4pZtH9tEOcCeHnCRqgxR+7wZYMiR/eOMIoKKqGFtBnqpyj2CW4ph8qULp4f1ghWOEjgVui1nNgOtGFtiugjXF; xm-page-viewid=ximalaya-web; impl=www.ximalaya.com.login; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1746547302,1746548230,1746714778,1747312830; HMACCOUNT=A06853B63764C5EA; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1747318263; cmci9xde=U2FsdGVkX1+RFZr3xXt5PuBkVqQm1VHHIyHs7jb/+YNO0+QSbtYfw/KDjmeRTKjGxqI8qpAfA83oBlzwrwBEQg==; pmck9xge=U2FsdGVkX19czV4ebIp9P3ROQrRdSu9z76B/L+ROvfc=; assva6=U2FsdGVkX1+X07TMTnfUfEEPX18CBu9twg7vYY1IoNc=; assva5=U2FsdGVkX187iblLMQxlvLVlLTDgTl+sV8PjfUWCzygEtkXABxwUia+7oUZ5iFeX9X0bnup1vZLddoMOHFvSiw==; vmce9xdq=U2FsdGVkX1+wvya4rfVA40Cb22Bebi0rttrGFy8yAa6QPh4WTC4IMVG44jcGa1pO6ZQs5iGqivnvqfztb+n1lJVKcf6BEc3t4WJNAjrbMss+Swm1XujuUfVX/6D8EaQL6dRE3w+L+zpsUXqtCqb03yUIkAQPUhDRD4BgenAIzmE=; web_login=1747322100285"
    }
            # 获取数据
            res = requests.get(url, headers=headers)
            res.encoding = "utf-8" 
            # print(res.headers.get("Content-Type"))
            # print(res.text)
            res_dict = res.json()
            res.raise_for_status()  # 检查请求是否成功
            # print(res_dict.keys())
            # print(res_dict["ret"])
            # print(res_dict["msg"])
            # print(res_dict["data"]["result"].keys())
            data = res_dict["data"]["result"]["response"]["docs"]
            # print(len(docs))
            # print(docs)                   
            # 在表格中显示数据
            self.display_data_in_table(data)
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("错误", f"请求失败: {str(e)}")
        except json.JSONDecodeError:
            messagebox.showerror("错误", "无法解析JSON数据，请确认API返回的是有效的JSON格式")
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误: {str(e)}")

    def display_data_in_table(self, data):
        """在表格中显示数据"""
        # 假设JSON数据是一个列表，每个元素是一个字典
        if not isinstance(data, list):
            messagebox.showwarning("警告", "JSON数据不是预期的列表格式")
            return
        
        if not data:
            messagebox.showinfo("提示", "没有找到相关数据")
            return
        
        # 遍历数据并添加到表格中，并使用enumerate自动生成序号   
        for index, item in enumerate(data, start=1):
            title = item["title"]
            author = item["nickname"]
            category = item["category_title"]
            ID = item["id"]
            vip = item["vipType"]
            # 添加序号列
            self.table.insert("", "end", values=(index, title, author, category, ID, vip))

if __name__ == "__main__":
    root = tk.Tk()
    app = Search(root)
    root.mainloop()