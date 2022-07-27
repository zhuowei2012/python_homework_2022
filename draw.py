# -*- coding:utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['SimHei'] # 用黑体显示中文
# 构建数据
x = [2, 4, 6, 8]
y = [450, 500, 200, 1000]
# 绘图
plt.bar(x=x, height=y, label='书库大全', color='steelblue', alpha=0.8)
# 在柱状图上显示具体数值, ha参数控制水平对齐方式, va控制垂直对齐方式
for x1, yy in zip(x, y):
     plt.text(x1, yy + 1, str(yy), ha='center', va='bottom', fontsize=20, rotation=0)
# 设置标题
plt.title("80小说网活跃度")
# 为两条坐标轴设置名称
plt.xlabel("发布日期")
plt.ylabel("小说数量")
# 显示图例
plt.legend()
# 画折线图
plt.plot(x, y, "r", marker='*', ms=10, label="a")
plt.xticks(rotation=45)
plt.legend(loc="upper left")
plt.savefig("a.jpg")
plt.show()