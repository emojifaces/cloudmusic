import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pyecharts.charts import Bar,Pie,Grid
from pyecharts import options as opts



csv_file = pd.read_csv('result/count_word_CN.csv',nrows=31)
word = csv_file['word'].tolist()
frequency = csv_file['frequency'].tolist()


bar = Bar(init_opts=opts.InitOpts(width='1200px',height='720px'))
bar.add_xaxis(word)
bar.add_yaxis("出现次数", frequency)
bar.set_global_opts(title_opts=opts.TitleOpts(title="中国rapper常用词汇"))
bar.render('test2.html')


# pie = (
#     Pie(init_opts=opts.InitOpts(width='1200px',height='720px'))
#     .add("", [list(z) for z in zip(word, frequency)])
#     .set_global_opts(title_opts=opts.TitleOpts(title="中国rapper"),
#                      legend_opts=opts.LegendOpts(pos_bottom='1px'),
#                      )
#     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
# )
#
#
# pie.render('test2.html')
