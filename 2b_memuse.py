import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import random
from tkinter import colorchooser
# データ準備
# in_data = [124, 60, 70, 133, 12, 19, 66, 52, 62, 2, 99, 82, 33]
in_data = []
in_data_len = 0
data = [[]]
data_len = 0
step = 0
max_step = 2000
is_sort = 0
auto_state = 0
auto_speed = 5
is_sorted = 0
start_color = [0, 1, 1]
end_color = [1, 0, 0]
only_swap = 0
guide_bar_color = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
]


def redraw():
    plt.cla()
    x = np.arange(in_data_len)
    y = data[step][3:]
    # bar_list = ax.bar(x, y, color="gray") #変更
    color_array = []
    for h in y:
        color_vector = [0, 0, 0]
        for i in range(3):
            color_vector[i] = start_color[i] + \
                (end_color[i]-start_color[i])/in_data_len*h
        color_array.append(color_vector)
    bar_list = ax.bar(x, y, color=color_array)
    if(data[step][0] != -1):  # [start,end,range]
        # data[step][0]はswap元を指す
        bar_list[data[step][0]].set_color(guide_bar_color[0])
        bar_list[data[step][1]].set_color(guide_bar_color[1])
        bar_list[data[step][2]].set_color(guide_bar_color[2])
    canvas.draw()


def array_set(len):
    global in_data
    in_data = []
    for i in range(1, len+1):
        # in_data.append(i)
        in_data.append(random.randint(0, len))
    global data
    data = [([-1, -1, -1]+in_data)]
    global is_sorted
    is_sorted = 0


def do_sort():
    global data
    data = [([-1, -1, -1]+in_data)]
    if(method.get() == "quick sort"):
        quickSort(0, len(in_data)-1)
    elif(method.get() == "simple sort"):
        simpleSort()
    data.append([-1, -1, -1]+data[-1][3:])
    global is_sorted
    is_sorted = 1
    global data_len
    data_len = len(data)


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
    if (is_sorted == 0):
        do_sort()
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
    if (is_sorted == 0):
        do_sort()
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
    global is_sorted
    if (is_sorted == 0):
        do_sort()
    global auto_state
    auto_state = (1-auto_state)


def btn_click_restart():
    print('restart')
    global step
    global stepstr
    step = 0
    stepstr.set("step="+str(step))
    redraw()


def btn_click_start_color():
    color = colorchooser.askcolor()
    print(color)
    global start_color
    for (i, j) in zip(color[0], range(3)):
        start_color[j] = i/255
    btn_start.config(fg=color[1])
    redraw()


def btn_click_end_color():
    color = colorchooser.askcolor()
    print(color)
    global end_color
    for (i, j) in zip(color[0], range(3)):
        end_color[j] = i/255
    btn_end.config(fg=color[1])
    redraw()


def change_length(num):
    pointer = num.find(".")
    global in_data_len
    in_data_len = int(num)
    array_set(in_data_len)
    btn_click_restart()


def auto_play():
    global auto_state
    if(auto_state):
        global step
        global stepstr
        if(step >= data_len-1):
            auto_state = 0
        else:
            step = step + 1 + data_len//100*auto_speed
            if(step >= data_len-1):
                step = data_len-1
            stepstr.set("speed="+str(auto_speed) +
                        ", step="+str(step))
            redraw()
    root.after(1, auto_play)


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
            if(only_swap == 0):
                data.append([left, right, i]+new_data)
        while(new_data[j] > pivot):
            j = j-1
            if(only_swap == 0):
                data.append([left, right, j]+new_data)
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
            if(only_swap == 0):
                data.append([i, j, minpos]+array)
        buffer = array[i]
        array[i] = array[minpos]
        array[minpos] = buffer
        data.append([i, j, minpos]+array)


if __name__ == "__main__":
    array_set(in_data_len)
    data[0] = ([-1]+in_data)
    root = tk.Tk()  # ウインドの作成
    root.title("sample")  # ウインドのタイトル
    root.geometry("1080x720")  # ウインドの大きさ
    combo = str()
    frame_1 = tk.Frame()
    frame_2 = tk.Frame()
    frame_3 = tk.Frame()
    frame_4 = tk.Frame()
    frame_5 = tk.Frame()

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
    label.pack(fill='none', padx=5, pady=4, in_=frame_1, side="top")
    label = tk.Label(root, text="default sort")
    label.pack(fill='none', padx=5, pady=4, in_=frame_2, side="top")
    label = tk.Label(root, text="sample length")
    label.pack(fill='none', padx=5, in_=frame_3, side="top")

    global method
    option = ["quick sort", "simple sort"]  # 選択肢
    method = tk.StringVar()
    label = ttk.Combobox(root, values=option,
                         textvariable=method, state="readonly", justify="center", width=10)
    label.bind("<<ComboboxSelected>>", method_selected)
    label.pack(fill='none', padx=5, in_=frame_1)

    global sort
    option = ["down", "up", "random"]  # 選択肢
    sort = tk.StringVar()
    label = ttk.Combobox(root, values=option,
                         textvariable=sort, state="readonly", justify="center", width=10)
    label.bind("<<ComboboxSelected>>", sort_selected)
    label.pack(fill='none', padx=5, in_=frame_2)

    scale = tk.Scale(
        root,
        orient=tk.HORIZONTAL,
        from_=0,
        to=512,
        command=change_length,
        showvalue=True,
        length=512/2
    )
    scale.pack(padx=20, fill=tk.X, in_=frame_3)

    stepstr = tk.StringVar()
    stepstr.set("step="+str(step))
    label = tk.Label(root, text="", textvariable=stepstr)
    label.pack(fill='none', padx=5, pady=4, side='bottom', in_=frame_5)

    # ボタン作成
    btn_start = tk.Button(root, text='start color', width=6, fg="#00FFFF", background='#00ffff',
                          command=btn_click_start_color)
    btn_start.pack(fill='none', padx=8, side='top', in_=frame_4)
    btn_end = tk.Button(root, text='end color', width=6, fg="#FF0000", background='#90caf9',
                        command=btn_click_end_color)
    btn_end.pack(fill='none', padx=8, side='bottom', in_=frame_4)

    btn = tk.Button(root, text='>', width=6, command=btn_click_next)
    btn.pack(fill='none', padx=8, side='right', in_=frame_5)
    btn = tk.Button(root, text='<', width=6, command=btn_click_back)
    btn.pack(fill='none', padx=8, side='right', in_=frame_5)
    btn = tk.Button(root, text='▷', width=6, command=btn_click_auto)
    btn.pack(fill='none', padx=8, side='right', in_=frame_5)
    btn = tk.Button(root, text='↩︎', width=6, command=btn_click_restart)
    btn.pack(fill='none', padx=8, side='right', in_=frame_5)

    frame_1.pack(side=tk.LEFT, expand=True)
    frame_2.pack(side=tk.LEFT, expand=True)
    frame_3.pack(side=tk.LEFT, expand=True)
    frame_4.pack(side=tk.LEFT, expand=True)
    frame_5.pack(side=tk.LEFT, expand=True)
    root.after(10, auto_play)
    root.mainloop()
