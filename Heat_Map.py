from sqlconnect import PyMySQL
# 瀵煎叆绯荤粺鍖�
import platform
from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts.charts import *

print("Python期末，热力图 \n")

x_index = ["2023-06-07", "2023-06-08", "2023-06-09", "2023-06-10", "2023-06-11", "2023-06-12", "2023-06-13"]
mydb = PyMySQL('localhost','root','ysj528528','chatbot')
ques_list = mydb.get_max_question()
y_index = list(reversed([row[0] for row in ques_list]))
y_value = mydb.get_index_max_question()
print(y_value)

def heatMap_charts() -> HeatMap():
    # 实例化对象
    heatMap = HeatMap()
    heatMap.add_xaxis(x_index)
    heatMap.add_yaxis("热度值", y_index, y_value, label_opts=opts.LabelOpts(is_show=True, position="inside"))
    # # 全局置标题、标签
    heatMap.set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle=""),
        legend_opts=opts.LegendOpts(type_="scroll", pos_top="5%"),
        visualmap_opts=opts.VisualMapOpts()
    )
    return heatMap

# 获取对象
p = heatMap_charts()
# 绘制图形，生成HTML文件的
p.render('static/templates/heatMap_charts.html')





