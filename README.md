<div align="center">

# RandomCall
简易的Python随机点名器
![GitHub repo size](https://img.shields.io/github/repo-size/Meltide/RandomCall)
![GitHub Repo stars](https://img.shields.io/github/stars/Meltide/RandomCall?style=flat)
![GitHub branch status](https://img.shields.io/github/checks-status/Meltide/RandomCall/main)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/Meltide/RandomCall)
![GitHub last commit](https://img.shields.io/github/last-commit/Meltide/RandomCall)
![GitHub Created At](https://img.shields.io/github/created-at/Meltide/RandomCall) 

</div>

## 使用方法
1. 确保你的Python版本为最新
2. 在本项目所在目录输入`pip install -r requirements.txt`
3. 输入`python main.py`即可启动

## 使用说明
- 程序会尝试加载默认文件 list.xlsx
- 如果未找到默认文件，请点击“文件 -> 导入”选择名单文件
- 点击点名按钮进行随机点名
- 点击退出按钮关闭程序

## 打包为.exe文件
1. 首先，请安装`pyinstaller`库
    ```
    pip install pyinstaller
    ```
2. 转到本项目所在的目录，输入以下命令
    ```
    pyinstaller -F -w main.py
    ```
3. 进入`dist`文件夹即可看到打包成的.exe文件