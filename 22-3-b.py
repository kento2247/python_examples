import tkinter as tk
import tkinter.ttk as ttk

folder_path = "/Users/tokurakento/Desktop/R3/109files/"
# folder_path = "109files/"
adjlist_path = folder_path+"adjlist.txt"
stations_path = folder_path+"stations.txt"
adjlist = open(adjlist_path, 'r', encoding='UTF-8')
stations = open(stations_path, 'r', encoding='UTF-8')

station_list = []  # visited, from, cost
is_visited = []
name_list = []
adj_list = []
root_list = []


def dijkstra(now, end):
    adj = adj_list[now]  # [to, cost]
    # print(f'adj={adj} from{now}')
    now_cost = station_list[now][2]
    for i in adj:  # [to, cost]
        to_station = i[0]
        to_cost = i[1]
        if(station_list[to_station][0]):
            # print(f"    station{to_station} is visited")
            continue
        cost = to_cost+now_cost
        target_cost = station_list[to_station][2]
        # print(f"    {now}-{to_station}, cost={cost}, tarcos={target_cost}")
        if cost < target_cost:
            station_list[to_station][1] = now  # from
            station_list[to_station][2] = cost
    minpos = [-1, float('inf')]
    for i in range(101):
        if(station_list[i][0] == 1):
            continue
        if(station_list[i][2] < minpos[1]):
            minpos[0] = i
            minpos[1] = station_list[i][2]
    if(minpos[0] == -1):
        return
    # print(f"    visit to station{minpos[0]}")
    station_list[minpos[0]][0] = 1
    dijkstra(minpos[0], end)


def set_adjpare_list():
    for station in stations.readlines():
        name = station.strip().split(" ")[1]
        name_list.append(name)
    for adj in adjlist.readlines():
        adj_pares = adj.strip().split(" ")
        pares_len = len(adj_pares)
        buf = []
        for j in range(1, pares_len):
            pare = adj_pares[j].split(",")
            # station_name = name_list[int(pare[0])-1]
            station_name = int(pare[0])-1  # 0オリジン
            cost = int(pare[1])
            buf.append([station_name, cost])
        adj_list.append(buf)
    # print(adj_list)


def set_root(begin, end):
    station_list.clear()
    for i in range(101):
        station_list.append([0, -1, float('inf')])  # visited, from, cost
    is_visited.clear()
    station_list[begin][0] = 1  # visited
    station_list[begin][2] = 0  # cost
    dijkstra(begin, end)
    pointer = end
    root_list.clear()
    while(1):
        root_list.append([pointer, station_list[pointer][2]])
        if(pointer == begin):
            break
        pointer = station_list[pointer][1]
    root_list.reverse()
    # print(root_list)


def show_result():
    error_flag = 0
    if(from_name.get() == ""):
        label_from.config(text='駅名が未入力です')
        error_flag = 1
    else:
        label_from.config(text='')
    if(to_name.get() == ""):
        label_to.config(text='駅名が未入力です')
        error_flag = 1
    else:
        label_to.config(text='')
    if(error_flag):
        return
    station_num = [-1, -1]
    for i in range(101):
        target_name = name_list[i]
        if(from_name.get() == target_name):
            station_num[0] = i
        if(to_name.get() == target_name):
            station_num[1] = i
    if(station_num[0] == -1):
        label_from.config(text='該当する駅名が存在しません')
        error_flag = 1
    else:
        label_from.config(text='')
    if(station_num[1] == -1):
        label_to.config(text='該当する駅名が存在しません')
        error_flag = 1
    else:
        label_to.config(text='')
    if(error_flag):
        return
    set_root(station_num[0], station_num[1])
    label_str = ""
    for i in range(len(root_list)):
        target_id = root_list[i][0]
        target_cost = root_list[i][1]
        label_str = label_str+f"{name_list[target_id]} {target_cost}分\n"
        if(i < len(root_list)-1):
            label_str = label_str + \
                f"  | {root_list[i+1][1]-target_cost}分\n"
    text.delete('1.0', 'end')
    text.insert("end", label_str)


def main():
    set_adjpare_list()
    width = 450
    height = 800

    root = tk.Tk()
    root.title("tokyu station")
    root.geometry(str(width)+"x"+str(height))

    frame_find = tk.Frame(root, pady=10, padx=5)

    frame_find_1 = tk.Frame(frame_find, pady=2, padx=5)
    label = tk.Label(frame_find_1, text="出発地")
    label.pack(side=tk.LEFT)
    global from_name
    from_name = tk.StringVar("")
    entry = tk.Entry(frame_find_1, textvariable=from_name, width=10)
    entry.pack(side=tk.RIGHT)
    frame_find_1.pack(side=tk.TOP)

    frame_find_1_mes = tk.Frame(frame_find, pady=0, padx=5)
    global label_from
    label_from = tk.Label(
        frame_find_1_mes, text="", fg="red")
    label_from.pack()
    frame_find_1_mes.pack(side=tk.TOP)

    frame_spacer = tk.Frame(frame_find, pady=0, padx=5)
    label = tk.Label(frame_spacer, text="")
    label.pack()
    frame_spacer.pack(side=tk.TOP)

    frame_find_2 = tk.Frame(frame_find, pady=2, padx=5)
    label = tk.Label(frame_find_2, text="目的地")
    label.pack(side=tk.LEFT)
    global to_name
    to_name = tk.StringVar("")
    entry = tk.Entry(frame_find_2, textvariable=to_name, width=10)
    entry.pack(side=tk.RIGHT)
    frame_find_2.pack(side=tk.TOP)

    frame_find_2_mes = tk.Frame(frame_find, pady=0, padx=5)
    global label_to
    label_to = tk.Label(frame_find_2_mes, text="", fg="red")
    label_to.pack(side=tk.BOTTOM)
    frame_find_2_mes.pack(side=tk.TOP)

    frame_find_3 = tk.Frame(frame_find, pady=25, padx=5)
    button = tk.Button(frame_find_3,
                       text="検索",
                       command=show_result
                       )
    button.pack()
    frame_find_3.pack(side=tk.TOP)

    frame_find.pack(side=tk.RIGHT)

    frame_result = tk.Frame(root, pady=10, padx=10)
    global text
    text = tk.Text(frame_result, padx=10, height=59)
    text.grid()
    frame_result.pack(side=tk.RIGHT)

    root.mainloop()


if __name__ == "__main__":
    main()
