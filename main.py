import tkinter as tk
import pandas as pd
from tkinter import messagebox, filedialog
import random
import os

# 初始化窗口
window = tk.Tk()
window.title("随机点名器")
x = int(window.winfo_screenwidth() / 2 - 200)
y = int(window.winfo_screenheight() / 2 - 100)
window.geometry(f"400x200+{x}+{y}")
window.resizable(0, 0) 
window.iconbitmap("icon.ico")

# 全局变量
name_list = []
var = tk.StringVar()

def load_names_from_file(file_path):
    # 从 Excel 文件加载名单
    try:
        df = pd.read_excel(file_path, usecols=[0], names=None)
        return [i[0] for i in df.values.tolist()]
    except Exception as e:
        messagebox.showerror("错误", f"无法读取文件：{e}")
        return []

def load_default_file():
    # 加载默认文件
    default_file = "list.xlsx"
    if os.path.exists(default_file):
        global name_list
        name_list = load_names_from_file(default_file)
        if name_list:
            var.set("默认名单已加载")
        else:
            var.set("默认名单为空")
    else:
        var.set("未找到默认名单，请手动导入")

def file_dialog():
    # 打开文件对话框选择 Excel 文件
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        global name_list
        name_list = load_names_from_file(file_path)
        if name_list:
            var.set("名单已加载")
        else:
            var.set("名单为空")
    else:
        var.set("未选择文件")

def start():
    # 随机选择一个名字
    if not name_list:
        var.set("名单为空")
        return
    random.shuffle(name_list)
    var.set(name_list[0])

def setup_menu():
    # 设置菜单栏
    main_menu = tk.Menu(window)
    menu_file = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="文件", menu=menu_file)
    menu_help = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="帮助", menu=menu_help)
    menu_file.add_command(label="导入", command=file_dialog)
    menu_file.add_separator()
    menu_file.add_command(label="退出", command=window.destroy)
    menu_help.add_command(label="帮助", command=lambda: messagebox.showinfo(
        "使用说明", "使用说明：\n"
        "1. 程序会尝试加载默认文件 list.xlsx\n"
        "2. 如果未找到默认文件，请点击“文件 -> 导入”选择名单文件\n"
        "3. 点击点名按钮进行随机点名\n"
        "4. 点击退出按钮关闭程序"))
    menu_help.add_command(label="关于", command=lambda: messagebox.showinfo(
        "关于", "随机点名器\n"
        "版本 1.0\n"
        "作者：Astral & Colipot\n"
        "Github 开源地址: github.com/Meltide/RandomCall"))
    window.config(menu=main_menu)

def setup_ui():
    # 设置界面
    tk.Label(window, textvariable=var, font=("黑体", 40, "bold"), fg="black").pack(pady=15)
    tk.Button(window, text="点名", height=2, width=20, font=("黑体", 20), relief="groove", bg="#A5D6A7", command=start).pack(pady=10)
    var.set("准备就绪")

# 主程序
load_default_file()  # 尝试加载默认文件
setup_menu()
setup_ui()
window.mainloop()