<<<<<<< HEAD
#-*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

class StatData():
     def __init__(self, info_list, x_title, y1_title, y2_title, title):
          self.info_list = info_list
          self.x_title = x_title
          self.y1_title = y1_title
          self.y2_title = y2_title
          self.title = title

     def drawBar(self):
          plt.rcdefaults()
          plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
          plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题

          info_list = self.info_list #[(u"小给", 88, 23), (u"小人", 78, 10), (u"小民", 90, 5), (u"小一", 66, 9), (u"小个", 80, 22), (u"小胶", 48, 5), (u"小带", 77, 19)]
          positions = np.arange(len(info_list))
          area_names = [row[0] for row in info_list]
          area_nums = [row[1] for row in info_list]
          area_avg_fee = [row[2] for row in info_list]

          fig, ax1 = plt.subplots()
          ax1.set_title(self.title)
          # 成绩直方图
          ax1.bar(positions, area_nums, width=0.6, align='center', color='r', label=self.y1_title)
          ax1.set_xticks(positions)
          ax1.set_xticklabels(area_names)
          ax1.set_xlabel(self.x_title)
          ax1.set_ylabel(self.y1_title)
          max_score = max(area_nums)
          ax1.set_ylim(0, int(max_score * 1.2))
          # 成绩标签
          for x,y in zip(positions, area_nums):
             ax1.text(x, y + max_score * 0.02, y, ha='center', va='center', fontsize=13)

          # 变动折线图
          ax2 = ax1.twinx()
          ax2.plot(positions, area_avg_fee, 'o-', label=self.y2_title)
          max_fee = max(area_avg_fee)
          # 变化率标签
          for x,y in zip(positions, area_avg_fee):
             ax2.text(x, y + max_fee * 0.02, ('%.2f' %y), ha='center', va= 'bottom', fontsize=13)
          # 设置纵轴格式
          fmt = '%.2f'
          yticks = mtick.FormatStrFormatter(fmt)
          ax2.yaxis.set_major_formatter(yticks)
          ax2.set_ylim(0, int(max_fee * 1.2))
          ax2.set_ylabel(self.y2_title)

          # 图例
          handles1, labels1 = ax1.get_legend_handles_labels()
          handles2, labels2 = ax2.get_legend_handles_labels()
          plt.legend(handles1+handles2, labels1+labels2, loc='upper right')

          plt.show()

     #暂时不用
     def dawnTopN(self, top_list):
          x_data = [f"{i}" for i in range(16, 21)]
          y_data = [random.randint(100, 300) for i in range(6)]

          # 正确显示中文和负号
          plt.rcParams["font.sans-serif"] = ["SimHei"]
          plt.rcParams["axes.unicode_minus"] = False

          # 画图，plt.bar()可以画柱状图
          for i in range(len(x_data)):
               plt.bar(x_data[i], y_data[i])
          # 设置图片名称
          plt.title("销量分析")
          # 设置x轴标签名
          plt.xlabel("年份")
          # 设置y轴标签名
          plt.ylabel("销量")
          # 显示
          plt.show()

if __name__ == '__main__':
     info_list = [(u"恩平市", 88, 13245.60), (u"鹤山市", 78, 11134.45), (u"江海区", 90, 9898.00), (u"开平市", 66, 12345.45), (u"蓬江区", 80, 18765.98), (u"台山市", 48, 15654), (u"新会区", 77, 18765)]
     stat_data = StatData(info_list, "区域", "签约数量", "签约价格", "江门市6月份房产签约统计数据")
=======
#-*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

class StatData():
     def __init__(self, info_list, x_title, y1_title, y2_title, title):
          self.info_list = info_list
          self.x_title = x_title
          self.y1_title = y1_title
          self.y2_title = y2_title
          self.title = title

     def drawBar(self):
          plt.rcdefaults()
          plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
          plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题

          info_list = self.info_list #[(u"小给", 88, 23), (u"小人", 78, 10), (u"小民", 90, 5), (u"小一", 66, 9), (u"小个", 80, 22), (u"小胶", 48, 5), (u"小带", 77, 19)]
          positions = np.arange(len(info_list))
          area_names = [row[0] for row in info_list]
          area_nums = [row[1] for row in info_list]
          area_avg_fee = [row[2] for row in info_list]

          fig, ax1 = plt.subplots()
          ax1.set_title(self.title)
          # 成绩直方图
          ax1.bar(positions, area_nums, width=0.6, align='center', color='r', label=self.y1_title)
          ax1.set_xticks(positions)
          ax1.set_xticklabels(area_names)
          ax1.set_xlabel(self.x_title)
          ax1.set_ylabel(self.y1_title)
          max_score = max(area_nums)
          ax1.set_ylim(0, int(max_score * 1.2))
          # 成绩标签
          for x,y in zip(positions, area_nums):
             ax1.text(x, y + max_score * 0.02, y, ha='center', va='center', fontsize=13)

          # 变动折线图
          ax2 = ax1.twinx()
          ax2.plot(positions, area_avg_fee, 'o-', label=self.y2_title)
          max_fee = max(area_avg_fee)
          # 变化率标签
          for x,y in zip(positions, area_avg_fee):
             ax2.text(x, y + max_fee * 0.02, ('%.2f' %y), ha='center', va= 'bottom', fontsize=13)
          # 设置纵轴格式
          fmt = '%.2f'
          yticks = mtick.FormatStrFormatter(fmt)
          ax2.yaxis.set_major_formatter(yticks)
          ax2.set_ylim(0, int(max_fee * 1.2))
          ax2.set_ylabel(self.y2_title)

          # 图例
          handles1, labels1 = ax1.get_legend_handles_labels()
          handles2, labels2 = ax2.get_legend_handles_labels()
          plt.legend(handles1+handles2, labels1+labels2, loc='upper right')

          plt.show()

     #暂时不用
     def dawnTopN(self, top_list):
          x_data = [f"{i}" for i in range(16, 21)]
          y_data = [random.randint(100, 300) for i in range(6)]

          # 正确显示中文和负号
          plt.rcParams["font.sans-serif"] = ["SimHei"]
          plt.rcParams["axes.unicode_minus"] = False

          # 画图，plt.bar()可以画柱状图
          for i in range(len(x_data)):
               plt.bar(x_data[i], y_data[i])
          # 设置图片名称
          plt.title("销量分析")
          # 设置x轴标签名
          plt.xlabel("年份")
          # 设置y轴标签名
          plt.ylabel("销量")
          # 显示
          plt.show()

if __name__ == '__main__':
     info_list = [(u"恩平市", 88, 13245.60), (u"鹤山市", 78, 11134.45), (u"江海区", 90, 9898.00), (u"开平市", 66, 12345.45), (u"蓬江区", 80, 18765.98), (u"台山市", 48, 15654), (u"新会区", 77, 18765)]
     stat_data = StatData(info_list, "区域", "签约数量", "签约价格", "江门市6月份房产签约统计数据")
>>>>>>> 23641a7f50235426062849e739737f441dccc69d
     stat_data.drawBar()