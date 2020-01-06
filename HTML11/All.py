import pandas as pd
import json
from flask import Flask, render_template, request
import pandas as pd
import cufflinks as cf
import plotly as py
import plotly.graph_objs as go
import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import Map
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Timeline
from pyecharts.charts import Bar
import dash
import dash_core_components as dcc
import dash_html_components as html

df1 = pd.read_csv("FemaleExecutives.csv", encoding='gbk')
df2 = pd.read_csv("canhui.csv", encoding='gbk')
df3 = pd.read_csv("School_enrollment_primary_and_secondary.csv", encoding='gbk')
df4 = pd.read_csv("womenManagement.csv", encoding='gbk')
df5 = pd.read_csv("canhuiduibi.csv", encoding='gbk')
df6 = pd.read_csv("lingdao.csv", encoding='gbk')
df7 = pd.read_csv('death_rate.csv', encoding='gbk')

# dict = { "世界各国日照率" : df3, "世界近年各国自杀率" : d2 ,"全球近年分年龄段自杀率" : d5, "全球近年男女参与劳动率" : d7,"全球近年性别自杀率":d6}#选择字典

x轴 = list(df5.set_index("Country").index)


# 图1
def map_world() -> Timeline:
    tl = Timeline()
    for i in range(2006, 2018):
        c = (
            Map()
                .add(
                "中小学女生与男生的入学比例（%）", list(zip(list(df3['CountryName']), list(df3["{}".format(i)]))), "world",
                is_map_symbol_show=False)
                #             .add("2017", [list(z) for z in zip(df3.CountryName, 女性受教育程度)], "world")
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="Map- 中小学女生与男生的入学比例（%）"),
                visualmap_opts=opts.VisualMapOpts(min_=0.9, max_=1.08),
            )
        )
        tl.add(c, "{}年".format(i))
    return tl


map_world().render_notebook()
map_world().render('1.html')


# 图2
def map_world1() -> Timeline:
    tl = Timeline()
    for i in range(2015, 2019):
        c = (
            Map()
                .add(
                "女性参会人数占比%", list(zip(list(df2['CountryName']), list(df2["{}".format(i)]))), "world",
                is_map_symbol_show=False)
                #         .add("2017", [list(z) for z in zip(df2.CountryName, 女性参会人数占比)], "world")
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="Map- 国家议会中妇女席位的比例（%）"),
                visualmap_opts=opts.VisualMapOpts(min_=7, max_=50),
            )
        )
        tl.add(c, "{}年".format(i))
    return tl


map_world1().render('2.html')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('whole_chart3.csv')

server = Flask(__name__)

# DASH页面
app1 = dash.Dash(__name__, server=server, url_base_pathname='/dash/', external_stylesheets=external_stylesheets)

app1.config.suppress_callback_exceptions = True
available_indicators = df['Indicator Name'].unique()

# markdown_text = """- 在追求性别平等的过程中，北欧国家继续领先世界。西欧的西班牙、非洲的埃塞俄比亚、拉丁美洲的墨西哥和东欧以及中亚地区的格鲁吉亚。这些国家在政治赋权方面有很大进步。
# 				   - 越来越多地女性可以使用现代方法满足计划生育的需要，而不是因为恶劣的医疗卫生环境导致孕产妇死亡
# """

app1.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content'),
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),
    html.Div(children=[
        dcc.Markdown('''
	## 领域对比
	#### 政治参与
	- 从政女性数量的大幅增加，但从比例上来看女性还是大大低于男性。
	- 东亚和太平洋地区在政治赋权方面性别差距继续扩大。
	- 在追求性别平等的过程中，北欧国家继续领先世界。西欧的西班牙、非洲的埃塞俄比亚、拉丁美洲的墨西哥和东欧以及中亚地区的格鲁吉亚。这些国家在政治赋权方面有很大进步。
	#### 就业
	- 括担任管理或领导职位的女性比例长期偏低，女性仍然未能获得与男性同等的就业机会	
	#### 医疗与健康
	- 越来越多地女性可以使用现代方法满足计划生育的需要，而不是因为恶劣的医疗卫生环境导致孕产妇死亡
	#### 教育
	东欧和中亚地区地区已经消除了教育领域的性别差距。
''')
    ])
])

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])


@app1.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]

    return {
        'data': [dict(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [dict(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app1.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app1.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)


regions_available = list(df2.CountryName.dropna().unique())
regions_available1 = list(df3.CountryName.dropna().unique())
data_str = df2.to_html()

with open("3.html", encoding="utf8", mode="r") as f:
    plot_all1 = "".join(f.readlines())
# with open("2.html", encoding="utf8", mode="r") as f:
# 	plot_all2 = "".join(f.readlines())
#
# 导入图表


regions_available_loaded = ['孕产妇死亡率（每10万例活产中所占比例）', '中小学女生与男生的入学比例（%）', '国家议会中妇女席位的比例（%）']  # 选框内容


@server.route('/', methods=['GET'])
def hello() -> 'html':
    return render_template('First.html',
                           the_title='女性权利可视化',
                           the_result=plot_all1,
                           # 						   the_result2 = plot_all2,
                           the_select_region=regions_available,  # 下拉选单
                           the_select_region1=regions_available_loaded,
                           the_res="""1. 北非，南亚和中亚五国中的土库曼斯坦、阿富汗斯坦与大洋洲岛国、东南亚地区除新马泰以外的国家孕妇死亡率较高。
					  \n2. 欧洲澳洲北美地区和东亚地区的孕妇死亡率较低。"""
                           )


@server.route('/query', methods=['GET', 'POST'])
def run_select() -> 'html':
    the_region = request.form["the_region_selected1"]  ## 取得用户交互输入
    print(the_region)
    # data_str = dict[the_region].to_html()#数据表

    # 制作图表切换效果
    if the_region == "中小学女生与男生的入学比例（%）":
        with open("1.html", encoding="utf8", mode="r") as f:
            plot_all3 = "".join(f.readlines())
            text = '同一教育阶段的女生正越来越获得与男生一样平等的教育机会。'
    elif the_region == "国家议会中妇女席位的比例（%）":
        with open("2.html", encoding="utf8", mode="r") as f:
            plot_all3 = "".join(f.readlines())
            text = '政治领域性别比例改善，从政女性数量的大幅增加。'
    elif the_region == "孕产妇死亡率（每10万例活产中所占比例）":
        with open("3.html", encoding="utf8", mode="r") as f:
            plot_all3 = "".join(f.readlines())
            text = """1. 北非，南亚和中亚五国中的土库曼斯坦、阿富汗斯坦与大洋洲岛国、东南亚地区除新马泰以外的国家孕妇死亡率较高。
					  \n2. 欧洲澳洲北美地区和东亚地区的孕妇死亡率较低。
					"""
    #     elif the_region=="全球近年性别自杀率":
    #         with open("1.html", encoding="utf8", mode="r") as f:
    #             plot_all3 = "".join(f.readlines())
    #
    #     elif the_region=="全球近年男女参与劳动率":
    #         with open("1.html", encoding="utf8", mode="r") as f:
    #             plot_all3 = "".join(f.readlines())

    regions_available1 = regions_available_loaded  # 下拉选单有内容
    return render_template('First.html',
                           the_title='世界女性权利可视化',
                           the_result=plot_all3,
                           the_res=text,
                           the_select_region=regions_available,  # 下拉选单
                           the_select_region1=regions_available_loaded
                           )


@server.route('/meeting', methods=['GET', 'POST'])
def hu_run_select() -> 'html':
    the_region = request.form["the_region_selected"]
    print(the_region)  # 检查用户输入
    dfs = df2.query("CountryName=='{}'".format(the_region))
    #     df_summary = dfs.groupby("行业").agg({"企业名称":"count","估值（亿人民币）":"sum","成立年份":"mean"}).sort_values(by = "企业名称",ascending = False )
    #     print(df_summary.head(5)) # 在后台检查描述性统计
    #     ## user select
    # print(dfs)
    #     # 交互式可视化画图
    fig = dfs.iplot(kind="bar", x="CountryName", asFigure=True)
    py.offline.plot(fig, filename="chart1.html", auto_open=False)

    #     # plotly.offline.plot(data, filename='file.html')
    with open("chart1.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())

    data_str = dfs.to_html()
    return render_template('results2.html',
                           the_title='国家议会女性人数占比（%）',
                           the_plot_all=plot_all,
                           # the_plot_all = [],
                           the_res=data_str,
                           the_select_region=regions_available,
                           )


@server.route('/female', methods=['GET', 'POST'])
def hu_run_select1() -> 'html':
    the_region = request.form["the_region_selected"]
    print(the_region)  # 检查用户输入
    dfs1 = df3.query("CountryName=='{}'".format(the_region))

    fig = dfs1.iplot(kind="bar", x="CountryName", asFigure=True)
    py.offline.plot(fig, filename="chart2.html", auto_open=False)

    with open("chart2.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())

    data_str = dfs1.to_html()
    return render_template('results2.html',
                           the_title='中小学女生与男生的入学比例（%）',
                           the_plot_all=plot_all,  # 图表
                           the_res=data_str,  # 表格
                           the_text=[],  # 文本
                           the_select_region=regions_available,
                           )


# @server.route('/dash',methods=['GET'])

# @server.route('/Match_analysis',methods=['GET','POST'])
# def hello3() -> 'html':
#
#
#     return render_template('Match_analysis.html',
#                            the_title='赛事分析',
#                            the_result=data3
#                            )
# @server.route('/The_table',methods=['GET','POST'])
# def hello4() -> 'html':
#
#
#     return render_template('The_table.html',
#                            the_title='积分榜',
#                            the_result=data4
#                            )
# @server.route('/Top_scorer',methods=['GET','POST'])
# def hello5() -> 'html':
#
#
#     return render_template('Top_scorer.html',
#                            the_title='射手榜',
#                            the_result=data_5
#                            )
# @server.route('/Competition_news',methods=['GET','POST'])
# def hello6() -> 'html':
#
#
#     return render_template('Competition_news.html',
#                            the_title='赛事新闻',
#                            the_result=data6
#                            )


# server.run(debug=True)
if __name__ == '__main__':
    server.run(debug=True)
