# アカウント作成
# https://chart-studio.plot.ly/Auth/login/#/
# APIを設定するために、ユーザ名とAPIキーを入力し以下を実行する


import pandas as pd 
nq = pd.read_csv(nq.csv)
nq.date = pd.to_datetime(nq.date)

# import plotly.express as px
# px.line()
import plotly
import plotly.graph_objects as go
plotly.tools.set_credentials_file(username="", api_key="")
from ipywidgets import widgets
# オフライン設定
plotly.offline.init_notebook_mode(connected=False)

# グラフのレイアウトを指定します。
# グラフのタイトルや、凡例の位置、第2軸を設定します。
layout = go.Layout(
    title="NQ",
    legend={"x":0.8, "y":0.1}, # 凡例の位置
    xaxis={"title":"Time: Week"}, # 範囲指定可能 , "range": [2010, 2016]
    yaxis={"title":"NQ", "rangemode":"tozero"}, # 0を含む
    width=1000, 
    height=600,
    font={"family":"Yu Gothic Bold, sans-selif", "size":20} # フォント
)

# 折れ線グラフ
# data = plotly.graph_objs.Scatter
data = go.Scatter(x=nq.date, y=nq.nq, mode="lines+markers", name="NQ")

# グリグリグラフ, 非公開設定
# http://python.zombie-hunting-club.com/entry/2017/11/03/223753#26-iplot%E3%83%A1%E3%82%BD%E3%83%83%E3%83%89%E3%81%AE%E3%82%AA%E3%83%97%E3%82%B7%E3%83%A7%E3%83%B3%E5%BC%95%E6%95%B0
fig = go.Figure(data=data, layout=layout)
plotly.offline.iplot(fig, filename="nq.html",  show_link=False, config={"displaylogo":False, "modeBarButtonsToRemove":["sendDataToCloud"]})　# fig.plot()
# plotly.offline.plot(fig, filename='name.html')
# sharing="secret",

# HTML化
# https://community.plot.ly/t/proper-way-to-save-a-plot-to-html/7063
# setting['asFigure'] = True  # dictオブジェクトにするために必要？
# fig = df.iplot(**setting)
# plotly.offline.plot(fig, filename='nq.html')  # ファイル名

# 棒グラフ
grp_data = go.Bar(x=nq.date, y=nq.grp)
fig = go.Figure(data=data, layout=layout)
plotly.offline.iplot(fig, filename="nq.html",  show_link=False, config={"displaylogo":False, "modeBarButtonsToRemove":["sendDataToCloud"]})　# fig.plot()