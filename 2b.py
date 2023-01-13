import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import random
import time

# データ準備
# in_data = [124, 60, 70, 133, 12, 19, 66, 52, 62, 2, 99, 82, 33]
in_data = []
in_data_len = 0
data = [[]]
step = 0
max_step = 2000
is_sort = 0
auto_state = 0
auto_speed = 8


def redraw():
    plt.cla()
    x = np.arange(len(in_data))
    y = data[step][3:]
    bar_list = ax.bar(x, y, color="gray")
    if(data[step][0] != -1):  # [start,end,range]
        # data[step][0]はswap元を指す
        bar_list[data[step][0]].set_color("red")
        bar_list[data[step][1]].set_color("red")
        bar_list[data[step][2]].set_color("blue")
    canvas.draw()


def array_set(len):
    global in_data
    in_data = []
    for i in range(1, len+1):
        # in_data.append(i)
        in_data.append(random.randint(0, len))


def do_sort():
    global data
    data = [([-1, -1, -1]+in_data)]
    if(method.get() == "merge sort"):
        # mergeSort(in_data)
        pass
    elif(method.get() == "quick sort"):
        quickSort(0, len(in_data)-1)
        # pass
    elif(method.get() == "simple sort"):
        simpleSort()
        # pass


def method_selected(event):
    print(method.get(), "was selected")
    do_sort()
    btn_click_restart()


def sort_selected(event):
    global data
    global in_data
    if(sort.get() == "up"):
        in_data.sort()
    elif (sort.get() == "down"):
        in_data.sort(reverse=True)
    else:
        random.shuffle(in_data)
    data = [([-1, -1, -1]+in_data)]
    btn_click_restart()
    do_sort()


def btn_click_next():
    print('next')
    global auto_state
    if(auto_state == 1):
        global auto_speed
        if(auto_speed == 10):
            return
        auto_speed += 1
    else:
        global step
        global stepstr
        if(step >= len(data)-1):
            return
        else:
            step = step+1
        stepstr.set("step="+str(step))
        redraw()


def btn_click_back():
    print('back')
    global auto_state
    if(auto_state == 1):
        global auto_speed
        if(auto_speed == 0):
            return
        auto_speed -= 1
    else:
        global step
        global stepstr
        if(step == 0):
            pass
        else:
            step = step-1
        stepstr.set("step="+str(step))
        redraw()


def btn_click_auto():
    print('auto')
    global auto_state
    auto_state = (1-auto_state)


def btn_click_restart():
    print('restart')
    global step
    global stepstr
    step = 0
    stepstr.set("step="+str(step))
    redraw()


def change_length(num):
    pointer = num.find(".")
    global in_data_len
    in_data_len = int(num[0:pointer])
    global lenstr
    lenstr.set("data length="+str(in_data_len))
    array_set(in_data_len)
    global data
    data = [([-1, -1, -1]+in_data)]
    btn_click_restart()


def auto_play():
    global auto_state
    if(auto_state):
        global step
        global stepstr
        if(step >= len(data)-1):
            auto_state = 0
        else:
            step = step+1
        stepstr.set("speed="+str(auto_speed) +
                    ", step="+str(step))
        redraw()
    root.after(10+(10-auto_speed)*50, auto_play)


def quickSort(left, right):
    if(left >= right):
        return
    new_data = data[-1][3:]
    pivot = new_data[(left+right)//2]
    i = left
    j = right

    while(i < j):
        while(new_data[i] < pivot):
            i = i+1
        while(new_data[j] > pivot):
            j = j-1
        if(i <= j):
            buffer = new_data[i]
            new_data[i] = new_data[j]
            new_data[j] = buffer
            i = i+1
            j = j-1
            data.append([left, right, i]+new_data)
    quickSort(left, j)
    quickSort(i, right)


def simpleSort():
    for i in range(len(in_data)):
        array = data[-1][3:]
        minpos = i
        for j in range(i, len(in_data)):
            if (array[minpos] > array[j]):
                minpos = j
        buffer = array[i]
        array[i] = array[minpos]
        array[minpos] = buffer
        data.append([i, i, minpos]+array)


def mergeSort(arr):
    if(len(data) >= max_step):
        print("over max sort step")
        return
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]

        mergeSort(L)
        mergeSort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


if __name__ == "__main__":
    array_set(in_data_len)
    data[0] = ([-1]+in_data)
    root = tk.Tk()  # ウインドの作成
    root.title("sample")  # ウインドのタイトル
    root.geometry("800x700")  # ウインドの大きさ
    combo = str()
    frame_left1 = tk.Frame()
    frame_left2 = tk.Frame()
    frame_right = tk.Frame()

    fig, ax = plt.subplots()
    x = np.arange(len(in_data))
    y = in_data
    ax.bar(x, y, color="gray")

    # tkinterのウインド上部にグラフを表示する
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # tkinterのウインド下部にツールを追加する
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    label = tk.Label(root, text="sort method")
    label.pack(fill='none', padx=20, pady=4, in_=frame_left1)
    label = tk.Label(root, text="default sort")
    label.pack(fill='none', padx=20, pady=4, in_=frame_left1)
    label = tk.Label(root, text="sample number")
    label.pack(fill='none', padx=20, in_=frame_left1)

    global method
    option = ["quick sort", "simple sort"]  # 選択肢
    method = tk.StringVar()
    label = ttk.Combobox(root, values=option,
                         textvariable=method, state="readonly")
    label.bind("<<ComboboxSelected>>", method_selected)
    label.pack(fill='none', padx=20, pady=4, in_=frame_left2)

    global sort
    option = ["down", "up", "random"]  # 選択肢
    sort = tk.StringVar()
    label = ttk.Combobox(root, values=option,
                         textvariable=sort, state="readonly")
    label.bind("<<ComboboxSelected>>", sort_selected)
    label.pack(fill='none', padx=20, in_=frame_left2)

    scale = ttk.Scale(
        root,
        orient=tk.HORIZONTAL,
        from_=0,
        to=512,
        command=change_length,
    )
    scale.pack(padx=10, fill=tk.X, in_=frame_left2)

    lenstr = tk.StringVar()
    lenstr.set("data length="+str(in_data_len))
    label = tk.Label(root, text="", textvariable=lenstr)
    label.pack(fill='none', padx=20, side='bottom', in_=frame_right)

    stepstr = tk.StringVar()
    stepstr.set("step="+str(step))
    label = tk.Label(root, text="", textvariable=stepstr)
    label.pack(fill='none', padx=20, pady=4, side='bottom', in_=frame_right)

    # ボタン作成
    btn = tk.Button(root, text='>', width=6, command=btn_click_next)
    btn.pack(fill='none', padx=8, side='right', in_=frame_right)
    btn = tk.Button(root, text='<', width=6, command=btn_click_back)
    btn.pack(fill='none', padx=8, side='right', in_=frame_right)
    btn = tk.Button(root, text='▷', width=6, command=btn_click_auto)
    btn.pack(fill='none', padx=8, side='right', in_=frame_right)
    btn = tk.Button(root, text='↩︎', width=6, command=btn_click_restart)
    btn.pack(fill='none', padx=8, side='right', in_=frame_right)

    frame_left1.pack(side=tk.LEFT, expand=True)
    frame_left2.pack(side=tk.LEFT, expand=True)
    frame_right.pack(side=tk.LEFT, expand=True)
    root.after(10, auto_play)
    root.mainloop()
