from flask import Flask, render_template
from datetime import datetime,timedelta
import aop
import aop.api
import json
from collections import Counter
from pyecharts import Bar, Line
from pyecharts import Page
from pyecharts import Overlap
from flask import request, jsonify
import time

# 设置网关域名
aop.set_default_server('gateway.open.umeng.com')

# 设置apiKey和apiSecurity
aop.set_default_appinfo(1046050, "0HKvp0jGmlp")


app = Flask("UMengData",static_folder="static",template_folder="templates")
#print(Flask.__doc__)
@app.route('/')
def index():
    return 'Hello World'

@app.route('/events')
def events():

    #构造Request和访问协议是否是https
    req = aop.api.UmengUappEventListRequest()
    #得到时间
    get_date = request.args.get("date")

    if is_valid_date(get_date) == False:
        now_date = datetime.now().strftime('%Y-%m-%d')
    else:
        now_date = get_date

    AndEvents = {}
    IosEvents = {}
    allEvents = {}

    resp = req.get_response(None, appkey="5c73a5e9f1f55699ab0000ef", startDate=now_date, endDate=now_date, perPage=30, page=1, version="")
    AndEvents[now_date] = {}
    for k in resp['eventInfo']:
        AndEvents[now_date][k['displayName']] = k['count']

    resp = req.get_response(None, appkey="5c76338bb465f50bc6001045", startDate=now_date, endDate=now_date, perPage=30, page=1, version="")
    IosEvents[now_date] = {}
    for k in resp['eventInfo']:
        IosEvents[now_date][k['displayName']] = k['count']

    x,y = Counter(AndEvents[now_date]),Counter(IosEvents[now_date])
    allEvents[now_date] = {}
    allEvents[now_date] = dict(x+y)

    resIosEvents = {}
    resAndEvents = {}
    for k in allEvents[now_date].keys() :
        if k not in AndEvents[now_date] :
            resAndEvents[k] = 0
        else:
            resAndEvents[k] = AndEvents[now_date][k]

        if k not in IosEvents[now_date] :
            resIosEvents[k] = 0
        else:
            resIosEvents[k] = IosEvents[now_date][k]


    page = Page()
    #处理渲染
    columns = list(allEvents[now_date].keys())


    #设置DAU数据
    data1 = list(resIosEvents.values())
    data2 = list(resAndEvents.values())
    data3 = list(allEvents[now_date].values())

    #设置柱状图的主标题与副标题
    bar = Bar("EVENTS", "完美世界电竞App的事件消息数:"+now_date)
    #添加柱状图的数据及配置项
    bar.add("IOS", columns, data1, is_more_utils=True,xaxis_label_textsize = 10, is_datazoom_show=True)
    bar.add("Android", columns, data2, is_more_utils=True,xaxis_label_textsize = 10)
    bar.add("全部", columns, data3,  is_more_utils=True,xaxis_label_textsize = 10,xaxis_interval=-10,xaxis_rotate=45)

    overlap = Overlap(height=600,width=1600)
    overlap.add(bar)

    page.add(overlap)

    #生成本地文件（默认为.html文件）
    return render_template('events.html',
                           myechart=page.render_embed(),
                           script_list=page.get_js_dependencies())

@app.route('/dau')
def dau():
    # 构造Request和访问协议是否是https
    appDAUQuest = aop.api.UmengUappGetActiveUsersRequest()
    appNEWQuest = aop.api.UmengUappGetNewUsersRequest()

    #计算时间
    now_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')

    #创建字典
    iosDAU = {}
    andDAU = {}
    allDAU = {}
    iosNEW = {}
    andNEW = {}
    allNEW = {}

    #IOS DAU
    respIOSDAU = appDAUQuest.get_response(None, appkey="5c76338bb465f50bc6001045", startDate=start_date, endDate=now_date, periodType="daily")
    for k in respIOSDAU['activeUserInfo']:
        iosDAU[k['date']] = k['value']

    #IOS NEW
    respIOSNEW = appNEWQuest.get_response(None, appkey="5c76338bb465f50bc6001045", startDate=start_date, endDate=now_date, periodType="daily")
    for k in respIOSNEW['newUserInfo']:
        iosNEW[k['date']] = k['value']

    #Android DAU
    respANDDAU = appDAUQuest.get_response(None, appkey="5c73a5e9f1f55699ab0000ef", startDate=start_date, endDate=now_date, periodType="daily")
    for k in respANDDAU['activeUserInfo']:
        andDAU[k['date']] = k['value']

    #Android NEW
    respANDNEW = appNEWQuest.get_response(None, appkey="5c73a5e9f1f55699ab0000ef", startDate=start_date, endDate=now_date, periodType="daily")
    for k in respANDNEW['newUserInfo']:
        andNEW[k['date']] = k['value']

    x,y = Counter(iosDAU),Counter(andDAU)
    allDAU = dict(x+y)

    x,y = Counter(iosNEW),Counter(andNEW)
    allNEW = dict(x+y)

    page = Page()
    #处理渲染
    columns = list(allDAU.keys())

    #设置DAU数据
    data1 = list(iosDAU.values())
    data2 = list(andDAU.values())
    data3 = list(allDAU.values())
    #设置NEW数据
    data4 = list(iosNEW.values())
    data5 = list(andNEW.values())
    data6 = list(allNEW.values())


    #设置柱状图的主标题与副标题
    bar = Bar("DAU", "完美世界电竞App最近一个月的DAU")
    #添加柱状图的数据及配置项
    bar.add("IOS", columns, data1, is_datazoom_show=True)
    bar.add("Android", columns, data2, is_datazoom_show=True)
    bar.add("全部", columns, data3, is_datazoom_show=True)

    line = Line("Line Chart Demo")
    line.add("全部", columns, data3, is_smooth=True)

    overlap = Overlap(height=500,width=1200)
    overlap.add(bar)
    overlap.add(line)


    #设置柱状图的主标题与副标题
    bar = Bar("NEW USER", "完美世界电竞App最近一个月的新增用户")
    #添加柱状图的数据及配置项
    bar.add("IOS", columns, data4, is_datazoom_show=True)
    bar.add("Android", columns, data5, is_datazoom_show=True)
    bar.add("全部", columns, data6, is_datazoom_show=True)

    line = Line("Line Chart Demo")
    line.add("全部", columns, data6, is_smooth=True)

    overlap2 = Overlap(height=500,width=1200)
    overlap2.add(bar)
    overlap2.add(line)

    page.add(overlap)
    page.add(overlap2)

    #生成本地文件（默认为.html文件）
    return render_template('bar.html',
                           myechart=page.render_embed(),
                           script_list=page.get_js_dependencies())


def is_valid_date(str):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, "%Y-%m-%d")
    return True
  except:
    return False

if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    app.run(host="0.0.0.0",port=5000,debug=True)