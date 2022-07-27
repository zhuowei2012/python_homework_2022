# *-* coding: utf-8 *-*
import os
import prettytable
from stat_data import StatData

grab_dir = "d:\\grab_data\\"
analys_dir = "d:\\stat_data\\"
post_fix = "_result.csv"

def get_area_nums_price(begin, end):
    info_list = []
    top_num_list = {}  #统计签约数量排名前10的小区
    for dirpath, dirnames, filenames in os.walk(grab_dir):
        for filename in filenames:
            area_name = filename.replace(post_fix, "")
            qy_count = 0  #按区域签约数量
            qy_price = 0  #按区域签约总单价
            #building_qy_count = 0 #按小区签约数量
            filepath = dirpath + filename
            with open(filepath, "r") as f:
                #跳过表头
                title_line = f.readline()
                if len(title_line) == 0:
                    print(f"{filepath} 是空文件")
                    continue
                #循环读取每一行
                while 1:
                    line = f.readline()
                    if len(line) == 0:
                        break
                    eles = line.split(",")
                    if eles[3] >= begin and eles[3] <= end:
                        print(line)
                        qy_count += 1
                        qy_price += float(eles[2])
                        building_qy_info = top_num_list.setdefault(area_name + "_" + eles[1], (0,0,0))
                        building_qy_count = building_qy_info[0] + 1
                        building_qy_price = float(building_qy_info[1]) + float(eles[2])
                        top_num_list[area_name + "_" + eles[1]] = (building_qy_count, building_qy_price,round(building_qy_price/building_qy_count, 2))

                if qy_count > 0:
                    info_list.append((area_name, qy_count, round(qy_price/qy_count, 2)))

    top_list = sorted(top_num_list.items(), key = lambda x : x[1][0], reverse=True)
    return info_list,top_list

if __name__ == '__main__':
    begin = "2022/6/1"
    end = "2022/6/30"

    info_list,top_num_list = get_area_nums_price(begin, end)
    st = StatData(info_list, "区域", "签约数量", "签约价格", f"江门市{begin}-{end}之间房产签约统计数据")
    st.drawBar()
    print(top_num_list)
    data = {}

    table = prettytable.PrettyTable(['排名', '区域', '楼盘名称', '签约数量', '签约均价'])
    index = 0
    for info in top_num_list:
        print(info)
        area_building = info[0].split("_")
        table.add_row([index+1, area_building[0], area_building[1], info[1][0], info[1][2]])
        index += 1

    print(table)





