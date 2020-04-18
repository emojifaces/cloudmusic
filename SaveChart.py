from pyecharts.charts import Bar,Pie
from pyecharts import options as opts
import pandas as pd


def save_to_bar(file,title,path,row):
    file = pd.read_csv(file, nrows=row)
    words = file['word'].tolist()
    frequency = file['frequency'].tolist()
    bar = Bar()
    bar.add_xaxis(words)
    bar.add_yaxis("出现次数", frequency)
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title))
    bar.render(path)

def save_to_pie(file,title,path,row):
    file = pd.read_csv(file, nrows=row)
    words = file['word'].tolist()
    frequency = file['frequency'].tolist()

    pie = (
        Pie(init_opts=opts.InitOpts(width='1200px',height='720px'))
        .add("", [list(z) for z in zip(words, frequency)])
        .set_global_opts(title_opts=opts.TitleOpts(title=title),
                         legend_opts=opts.LegendOpts(pos_bottom='1px'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    pie.render(path)