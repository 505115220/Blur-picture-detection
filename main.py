import cv2
import os
import numpy as np
import tkinter
from tkinter import *
import ttkbootstrap as ttk
import time


def get_file_path():
    # 无问题
    # 用于接收和分割处理输入的多个路径，并在所有文件路径中进行筛选，最后输出符合要求的文件的绝对路径
    file_path = E1.get()
    real_p = file_path.split(',')
    # real_p是一个包含多个路径的列表
    path_name = []
    path_name2 = []
    for pp in real_p:  # 对于每一个总目录有如下
        for dirpath, dirnames, filenames in os.walk(pp):  #
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                path_name.append(path)  # 获取到每一个总目录下的所有文件路径
    #  对于多个总目录的全部文件路径，根据后缀进行筛选
    for d in path_name:
        if os.path.splitext(d)[1] in (".jpg", ".JPG", ".PNG", ".png",".raw", ".RAW", ".jpeg", ".JPEG", ".gif", ".GIF", ".tif", ".tiff", ".TIF", ".TIFF"):
            # 需要筛选的文件后缀名
            path_name2.append(d)  # 返回筛选到的文件路径
    return  path_name2


def batch(path_name2, blur_value, show_pic, result_path):
    file_path_list = []
    path_name = []
    blur_path = []
    for i in range(len(path_name2)):
        image = cv2.imdecode(np.fromfile(path_name2[i], dtype=np.uint8), cv2.IMREAD_COLOR)
        height, width, _ = image.shape
        size = (int(width*0.85), int(height*0.85))
        image = cv2.resize(image, size)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        if str(fm) < str(blur_value):
            text = "Blurry"
            cv2.putText(image, "{}: {:.2f}".format(text, fm), (30, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 0, 255), 20)
            blur_path.append(path_name2[i])
        else:
            text = "Good!"
            cv2.putText(image, "{}: {:.2f}".format(text, fm), (30, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 255, 0), 20)
        if show_pic:
            cv2.namedWindow("Image", 0)
            cv2.resizeWindow("Image", int(width*0.1), int(height*0.1))
            cv2.imshow("Image", image)
            cv2.waitKey(250)
            cv2.destroyAllWindows()
        i = i + 1
    p = result_path + "\模糊度.csv"
    with open(p, 'w', encoding='utf-8-sig') as f1:
        f1.write('\n'.join(blur_path))
        

def main_app():
    start = time.time()  # 开始计时
    file_path = get_file_path()
    blur_value = get_blur_value()
    show_pic =  get_show_pic()
    result_path = get_result_path()
    batch(file_path, blur_value, show_pic, result_path)
    end = time.time()  # 开始计时
    t3 = str('检测用时:') + '%.2f' % (end - start) + str("s")
    text.insert(END, t3 + '\n')
    text.insert(END, "检测完成！" + '\n')

def open_path():
    path = get_result_path()
    dirtion = os.path.dirname(path+"\\")
    os.system('start ' + dirtion)

def close_window():
    root.destroy()


def get_blur_value():
    get_blur_value = E3.get()
    return get_blur_value

def get_show_pic():
    if show_pic.get() == True:
        return True
    else:
        return False

def get_result_path():
    get_result_path = E2.get()
    return get_result_path

# 主界面
root = ttk.Window()
root.title("模糊图片检测程序")
root.geometry("540x350+600+400")
root.resizable(False, False)
menu = tkinter.Menu(root, tearoff=False)
about_menu = tkinter.Menu(menu, tearoff=False)
root.config(menu=menu)
#按钮功能布置
L1 = ttk.Label(root, text="请输入需要检测照片的目录路径:")
L1.grid(row=0, column=0, columnspan=3, sticky='snw')
E1 = ttk.Entry(root, bootstyle='success')
E1.grid(row=1, column=0, columnspan=3, ipadx=188, padx=5, pady=2, sticky='snew')

L2 = ttk.Label(root, text="请输入导出检测结果的目录路径:")
L2.grid(row=2, column=0, columnspan=3, sticky='snw')
E2 = ttk.Entry(root, bootstyle='success')
E2.grid(row=3, column=0, columnspan=3, ipadx=188, padx=5, pady=2, sticky='snew')
B3 = tkinter.Button(root, text="打开检测结果目录", command=open_path)
B3.grid(row=4, column=2, ipadx=20, sticky='sne', padx=5, pady=2)

L3 = tkinter.Label(root, text="请输入检测阈值:")
L3.grid(row=5, column=0, sticky='snw')
E3 = ttk.Spinbox(root, from_=1, to=200, increment=1, width=10)
E3.insert(0, "10")
E3.grid(row=5, column=0, padx=5, pady=2, sticky="nse")

B4 = tkinter.Button(root, text="开始", command=lambda: main_app())
B4.grid(row=6, column=2, ipadx=20, sticky='sne', padx=5, pady=2)
B4 = tkinter.Button(root, text="退出", command=close_window)
B4.grid(row=7, column=2, ipadx=20, sticky='sne', padx=5, pady=2)
L4 = tkinter.Label(root, text="运行状态:")
L4.grid(row=7, column=0, sticky='snw')

show_pic = tkinter.BooleanVar()
C5 = ttk.Checkbutton(root, text="是否显示检测过程", variable=show_pic, onvalue="True", offvalue="False")
C5.grid(row=6, column=0, padx=5, pady=1, sticky="nse")

text = Text(root, width=40, height=10)
text.grid(row=8, column=0, columnspan=4, padx=1, pady=1, sticky='snew')
root.mainloop()
