# *-* coding: utf-8 *-*

# encoding:UTF-8
from bs4 import BeautifulSoup
import requests
import time
import json
import re
#import datetime
import os

url_root = 'http://jmzjj.jiangmen.cn:8085/'
api = 'api/TradeInfoJMApi/GetSPFYSXM'
query_type = "ysxmmc"  #表示传入的查询条件是预售项目名称，本项目不使用，只做入参，其他的忽略


# 获取每个区的URL
def get_area_links(area):
    urls = {}
    list_view = []
    #print('list_view:{}'.format(list_view))
    wb_data = requests.get(url_root)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    list_view = [x for x in str(soup.find_all(id="townentry")[0]).split("\n") if x.startswith("<a")]
    print(list_view)
    for list_url in list_view :
        index0 = list_url.find(r"?jgid")
        index1 = list_url.find(r'">')
        index2 = list_url.find(r'&')
        index3 = list_url.find(r"</a>")
        if index0 != -1 and index1 !=-1 and index2 != -1 and index3 !=-1:
            cur = list_url[index1+2:index3]
            if len(area) > 0 and cur != area:
                continue
            urls[cur] = list_url[index0:index2]
    return urls

# 获取每个区的所有预售项目列表中每个项目的URL（注意要考虑翻页，并且要考虑去重），key不是楼盘，可能是楼盘下的某一栋，因为是不同的预售证
#/public/web/ysxm_JM?ysxmid=C7D32441F7414CA998FC33B9D3E13367&jgid=a28d3522-f93f-46b7-9446-1ccbfd3b5146
def get_project_links(area=''):
    urls = get_area_links(area)
    print(urls)

    area_project_url_list = {}
    project_url_list = {}
    pageindex = 1
    pagesize = 10
    for cur_area,area_url in urls.items():
        pageindex = 1
        project_url_list = {}
        while 1:
            #time.sleep(1)
            url = f"{url_root}{api}{area_url}&type={query_type}&value=&pageindex={pageindex}&pagesize={pagesize}"
            wb_data = requests.get(url)
            project_info = safe_json_loads(wb_data.text)
            print(project_info)
            if project_info["Succeed"] != '1':
                print(f"读取{cur_area}:{url}失败")
                continue
            #nums = project_info["Data"]["total_count"]
            rows = project_info["Data"]["rows"]
            for row in rows:
                row_data = row["data"]
                doorplate = row_data[0]  #门牌号
                project_info = row_data[1]
                project_url = project_info[9:project_info.find("\' target=")]   #项目名称链接
                project_name = project_info[project_info.find(">")+1: project_info.rfind("<")]  #项目名称
                #如果需要预售许可证，这里加
                #to do
                #按门牌号，否则可能会漏
                project_url_list[doorplate] = project_url

            if len(rows) < pagesize:
                break
            pageindex += 1
            #测试代码，只跑第一页
            #if pageindex > 1:
            #    break

        #得到当前区域的所有楼盘的链接
        print(project_url_list)
        area_project_url_list[cur_area] = project_url_list

        #测试代码，只跑一个区
        #break
    return area_project_url_list
    '''
        soup = BeautifulSoup(wb_data.text, 'lxml')
        # print soup.select('infolist > div > table > tbody > tr.article-info > td.t > span.pricebiao > span')   ##infolist > div > table > tbody > tr.article-info > td.t > span.pricebiao > span
        print
        soup.select('span[class="price_now"]')[0].text
        print
        soup.select('div[class="palce_li"]')[0].text
        # print list(soup.select('.palce_li')[0].stripped_strings) if soup.find_all('div','palce_li') else None,  #body > div > div > div > div > div.info_massege.left > div.palce_li > span > i
        data = {
            'title': soup.title.text,
            'price': soup.select('span[class="price_now"]')[0].text,
            'area': soup.select('div[class="palce_li"]')[0].text if soup.find_all('div', 'palce_li') else None,
            'date': soup.select('.look_time')[0].text,
            'cate': '个人' if who_sells == 0 else '商家',
        }
        print(data)
        result = json.dumps(data, encoding='UTF-8', ensure_ascii=False)  # 中文内容仍然无法正常显示。 使用json进行格式转换，然后打印输出。
        print
        result
    '''

#private，返回第三级楼盘和楼盘下所有url的数据，入参是get_project_links返回的内容
def get_item_all_info(area_project_urls):
    #if 1:
    for cur_area, projectInfos in area_project_urls.items():
        building_no_list = []
        for project, project_url in projectInfos.items():
            print(f"开始分析 {project} 楼盘...")
            items_urls = []
            #data_url = "http://jmzjj.jiangmen.cn:8085/public/web/ysxm_JM?ysxmid=D50524B8C8E447CA8FCD2E2DD0F4C9FF&jgid=91679226-6e6c-4b90-b60f-6f4b87291133"
            data_url = f"{url_root}{project_url}"
            wb_data = requests.get(data_url)
            #print(wb_data.text)
            soup = BeautifulSoup(wb_data.text, 'lxml')
            project_name = str(soup.find_all(id="PresellName")[0])
            index0 = project_name.rfind("</a>")
            index1 = project_name.rfind('">')
            project_name = project_name[index1+2 : index0]

            #找到栋号，因为这里可能重复，所以要根据栋号来去重
            building_no = str(soup.find_all(id="table33")[0])
            key_words_0 = '<tr '
            key_words_1 = '<td '
            index4 = 0
            #跳过表头，先找到第二行
            for i in range(2):
                index4 = building_no.find(key_words_0, index4+2)
                #print(f"第{i}次{index4}")
            #继续找第3列和第5列
            while index4 != -1:
                index4_td3 = index4  #行开头
                #本行第3列
                for i in range(3):
                    index4_td3 = building_no.find(key_words_1, index4_td3+2)
                index4_0 = building_no.find(">", index4_td3)
                index4_1 = building_no.find("</td>", index4_td3)
                #得到第3列的值:
                building_name = building_no[index4_0 + 1: index4_1]
                #print(building_name)
                if building_name in building_no_list:
                    #跳过此行
                    print("f{building_name} 这个楼已经分析过了，跳过。")
                    index4 = building_no.find(key_words_0, index4 + 2)
                    continue

                building_no_list.append(building_name)
                print(f"开始分析 {building_name} 这个楼...")
                #本行第5列的"进入"链接
                index4_td5 = index4_td3
                index4_td5 = building_no.find("<a href=", index4_td5+2)
                index4_td5_end = building_no.find("=ysxm", index4_td5)
                item_rul = building_no[index4_td5 + 9 : index4_td5_end + 5]
                item_rul = item_rul.replace("&amp;", "&")
                items_urls.append(item_rul)

                #开始找下一行
                index4 = building_no.find(key_words_0, index4 + 2)

            #print(building_no)
            #print("index4:", index4)
            #index4_0 = building_no.find(">", index4)
            #index4_1 = building_no.find("</td>", index4)
            #building_no = building_no[index4_0+1 : index4_1]
            #print(building_no)
            #building_no_list.append(building_no)

            #直接找到“进入”的链接
            #project_infos = soup.find_all(href=re.compile("lpb"))
            #for project_info in project_infos:
                #    project_info = str(project_info).replace("&amp;", "&")
                #    index3 = project_info.find("=ysxm")
                #    item_rul = project_info[9:index3+5]
                #    #print(item_rul)
            #    items_urls.append(item_rul)

            house_detail = get_detail(items_urls)
            lines = []
            for house_info in house_detail:
                #print(house_info)
                #print(f"{project_name}:签约单价:{house_info[0]},签约日期:{house_info[1]}")
                lines.append(f"{cur_area},{project_name},{house_info[0]},{house_info[1]}")
            save_to_file(cur_area, lines)
            #print(project_infos)
    #return items_urls

#根据传入的url，获取每个url下网签的套数，均价
def get_detail(url_list):
    house_detail = []
    for url in url_list:
        data_url = f"{url_root}api/GzymApi/LpbNew?{url[4:]}&xmlx=0&jgid="
        wb_data = requests.get(data_url)
        #print(wb_data.text)
        #soup = BeautifulSoup(wb_data.text, 'lxml')
        house_infos = safe_json_loads(wb_data.text)["Data"]["fw"]
        #print(house_infos)
        #得到每个已经签约的房子的单价、签约日期
        count_11 = 0
        for house_info in house_infos:
            if house_info["fwztMc"] == '已备案' or house_info["fwztMc"] == '已签订':
                #house_info = str(house_info).replace("&amp;", "&")
                #print(house_info)
                count_11 += 1
                if count_11 == 10:
                    time.sleep(1)
                    count_11 = 0
                cur_url = f"{url_root}public/web/h?ljzid={house_info['ljzid']}&fwbm={house_info['fwbm']}&" \
                          f"ysxmid={house_info['ysxmid']}&winWidth=1100"
                Refer = f"{url_root}public/web/{url}"
                #print("Refer:", Refer)
                headers = {"Referer": Refer}
                try:
                    wb_data1 = requests.get(cur_url, headers=headers)
                except Exception:
                    print("网络断开！需要重连")
                    wb_data1 = requests.get(cur_url, headers=headers)

                #print(wb_data1.text)
                soup = BeautifulSoup(wb_data1.text, 'lxml')
                sbdj = str(soup.find_all(id="sbdj")[0])
                dj_index0 = sbdj.find("元")
                dj_index1 = sbdj.find(">")
                #print(sbdj)
                sbdj = sbdj[dj_index1+1:dj_index0]
                qyrq = str(soup.find_all(id="VisaDate")[0])
                qyrq_index0 = qyrq.find(">")
                qyrq_index1 = qyrq.find(" ", qyrq_index0)
                qyrq = qyrq[qyrq_index0+1:qyrq_index1]
                print(f"{house_info['fh']},{house_info['fwztMc']}, 签约单价:{sbdj},签约日期:{qyrq}")
                house_detail.append((float(sbdj),qyrq))
    print(house_detail)
    return house_detail

def safe_json_loads(data_str):
    try:
        data_str = data_str.replace(r"\"", r"'")
        data_str = data_str.replace("\\", "")
        result = json.loads(data_str)
        #print("最终json加载结果：{}".format(result))
        return result
    except Exception as e:
        #print("异常信息e：{}".format(e))
        error_index = re.findall(r"char (\d+)\)", str(e))
        if error_index:
            error_str = data_str[int(error_index[0])]
            data_str = data_str.replace(error_str, "")
            #print("替换异常字符串{} 后的文本内容{}".format(error_str, data_str))
            # 该处将处理结果继续递归处理
            return safe_json_loads(data_str)
# get_item_info(url)

#保存到文件
def save_to_file(area, lines):
    title = ",".join(["区县","楼盘名称", "网签价格","网签日期"]) + "\n"
    filename = './' + area +'_result.csv'
    if os.path.exists(filename):
        title = ""
    with open(filename, "a") as f:
        f.write(title);
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    # get_links_from(1)
    projectLinks = get_project_links("蓬江区")
    print("*"*56)
    print(projectLinks)
    items_urls = get_item_all_info(projectLinks)
    #get_detail(items_urls)
    #get_project_links()
    # get_classify_url()