folder_path = "/Users/tokurakento/Desktop/R3/109files/"
# folder_path = "109files/"
adjlist_path = folder_path+"adjlist.txt"
stations_path = folder_path+"stations.txt"
adjlist = open(adjlist_path, 'r', encoding='UTF-8')
stations = open(stations_path, 'r', encoding='UTF-8')

station_list = []  # visited, from, cost
is_visited = []
for i in range(101):
    station_list.append([0, -1, float('inf')])  # visited, from, cost
name_list = []
adj_list = []


def dijkstra(now, end):
    adj = adj_list[now]  # [to, cost]
    print(f'adj={adj} from{now}')
    now_cost = station_list[now][2]
    for i in adj:  # [to, cost]
        to_station = i[0]
        to_cost = i[1]
        if(station_list[to_station][0]):
            print(f"    station{to_station} is visited")
            continue
        cost = to_cost+now_cost
        target_cost = station_list[to_station][2]
        print(f"    {now}-{to_station}, cost={cost}, tarcos={target_cost}")
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
    print(f"    visit to station{minpos[0]}")
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


def main():
    begin = (1)-1
    end = (71)-1
    set_adjpare_list()
    station_list[begin][0] = 1  # visited
    station_list[begin][2] = 0  # cost
    dijkstra(begin, end)
    pointer = end
    while(1):
        print(
            f"TY{pointer+1} {name_list[pointer]}, cost={station_list[pointer][2]}")
        if(pointer == begin):
            break
        pointer = station_list[pointer][1]


if __name__ == "__main__":
    main()
