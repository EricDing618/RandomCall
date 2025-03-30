import tkinter as tk
import pandas as pd
from tkinter import messagebox, filedialog
import random
import os
import base64
from io import BytesIO
from PIL import Image, ImageTk

# 初始化窗口
window = tk.Tk()
window.title("RandomCall")
window.configure(bg="white")
x = int(window.winfo_screenwidth() / 2 - 200)
y = int(window.winfo_screenheight() / 2 - 112)
window.geometry(f"400x225+{x}+{y}")
window.resizable(0, 0)

# 设置窗口图标
img_code = r"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"
icon_data = base64.b64decode(img_code)
icon_image = Image.open(BytesIO(icon_data))
icon_photo = ImageTk.PhotoImage(icon_image)
window.iconphoto(True, icon_photo)

def new_window():
    # 关于窗口
    about = tk.Toplevel(window)
    about.focus_force()
    about.title("关于")
    about_x = int(window.winfo_screenwidth() / 2 - 150)
    about_y = int(window.winfo_screenheight() / 2 - 100)
    about.geometry(f"300x200+{about_x}+{about_y}")
    about.configure(bg="white")
    about.resizable(0, 0)

    about_var = tk.StringVar()

    tk.Label(about, text="RandomCall", font=("Tahoma", 30, "bold"), bg="white").pack(padx=5, pady=5, anchor="nw")
    tk.Label(about, text="简易的Python随机点名器", font=("黑体", 12), bg="white").pack(padx=5, anchor="nw")
    t = tk.Text(about, height=50, font=("Arial", 10), bg="white", relief="groove")
    t.pack(padx=5, pady=5, anchor="nw")
    t.insert("end",
             "版本 1.2\n\n"
             "作者: Github@Meltide\n"
             "开源地址: github.com/Meltide/RandomCall")
    t.config(state="disabled")

# 全局变量
name_list = []
called_name_list = []
var = tk.StringVar()
check_var = tk.IntVar()
text_status = 0
animation_running = False

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
    file_path = filedialog.askopenfilename(title="导入名单", filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")])
    if file_path:
        global name_list
        name_list = load_names_from_file(file_path)
        if name_list:
            var.set("名单已加载")
        else:
            var.set("名单为空")
    else:
        var.set("未选择文件")

def animate_name():
    # 动画效果：不断变换名字
    global animation_running
    if not animation_running or not name_list:
        return
    random_name = random.choice(name_list)
    var.set(random_name)
    window.after(65, animate_name)

def start():
    # 随机选择一个名字
    global animation_running
    if not name_list:
        if called_name_list:
            var.set("名单已用完")
        else:
            var.set("名单为空")
        return
    if not animation_running:
        animation_running = True
        animate_name()
        window.after(800, stop_animation) 

def stop_animation():
    # 停止动画并显示最终名字
    global animation_running
    animation_running = False
    if name_list:
        selected_name = name_list.pop(0)
        var.set(selected_name)
        called_name_list.append(selected_name)
        if not name_list:
            var.set("名单已用完")

def reset():
    global name_list, called_name_list
    # 清空已点名的名单
    called_name_list.clear()
    # 重新加载默认名单
    load_default_file()
    if name_list:
        var.set("准备就绪")
    else:
        var.set("名单为空")

def called_name_list_show():
    # 显示已点名名单
    if check_var.get() == 0:
        if called_name_list:
            messagebox.showinfo("已点名名单", ", ".join(called_name_list))
        else:
            messagebox.showinfo("已点名名单", "没有已点名名单")
    else:
        messagebox.showinfo("已点名名单", "允许重复点名时，已点名名单不显示")

def setup_menu():
    # 设置菜单栏
    main_menu = tk.Menu(window)
    menu_file = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="文件", menu=menu_file)
    menu_help = tk.Menu(main_menu, tearoff=0)
    main_menu.add_cascade(label="帮助", menu=menu_help)
    menu_file.add_command(label="已点名名单", command=called_name_list_show)
    menu_file.add_command(label="导入名单", command=file_dialog)
    menu_file.add_separator()
    menu_file.add_command(label="退出", command=window.destroy)
    menu_help.add_command(label="帮助", command=lambda: messagebox.showinfo(
        "使用说明", "使用说明：\n"
        "1. 程序会尝试加载默认文件 list.xlsx\n"
        "2. 如果未找到默认文件，请点击“文件 -> 导入”选择名单文件\n"
        "3. 可以选择是否允许重复点名\n"
        "4. 点击“点名”按钮进行随机点名\n"
        "5. 点击“重置”按钮清空已点名名单\n"
        "6. 点击“文件 -> 已点名名单”查看已点名名单\n"))
    menu_help.add_command(label="关于", command=new_window)
    window.config(menu=main_menu)

def setup_ui():
    # 设置界面
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)
    tk.Label(window, textvariable=var, font=("黑体", 40, "bold"), fg="black", bg="white").grid(row=0, column=0, columnspan=2, pady=10)
    tk.Checkbutton(window, text="允许重复点名", variable=check_var, onvalue=1, offvalue=0, bd=0, bg="white").grid(row=1, column=0, columnspan=2)
    tk.Button(window, text="点名", height=2, width=12, font=("黑体", 20), relief="flat", bd=0, bg="#A5D6A7", activebackground="#43A047", command=start).grid(row=2, column=0, pady=10)
    tk.Button(window, text="重置", height=2, width=12, font=("黑体", 20), relief="flat", bd=0, bg="#A5D6A7", activebackground="#43A047", command=reset).grid(row=2, column=1, pady=5)
    var.set("准备就绪")

# 主程序
load_default_file()
setup_menu()
setup_ui()
window.mainloop()