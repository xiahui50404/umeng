# -*- coding: utf-8 -*-
#!/usr/bin/env python

import aop
import aop.api
import json
from datetime import datetime,timedelta
from collections import Counter

# 设置网关域名
aop.set_default_server('gateway.open.umeng.com')

# 设置apiKey和apiSecurity
aop.set_default_appinfo(1046050, "0HKvp0jGmlp")

# 构造Request和访问协议是否是https
req = aop.api.UmengUappEventListRequest()
AndEvents = {}
IosEvents = {}
allEvents = {}

# 发起Api请求
try:
    #now_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() + timedelta(days=-2)).strftime('%Y-%m-%d')
    #for i in [0,1,2,3,4,5,6,7]:
    i = 0
    now_date = (datetime.now() + timedelta(days=-i)).strftime('%Y-%m-%d')

    resp = req.get_response(None, appkey="5c73a5e9f1f55699ab0000ef", startDate=now_date, endDate=now_date, perPage=10, page=1, version="")
    AndEvents[now_date] = {}
    for k in resp['eventInfo']:
        AndEvents[now_date][k['displayName']] = k['count']

    resp = req.get_response(None, appkey="5c76338bb465f50bc6001045", startDate=now_date, endDate=now_date, perPage=10, page=1, version="")
    IosEvents[now_date] = {}
    for k in resp['eventInfo']:
        IosEvents[now_date][k['displayName']] = k['count']

    x,y = Counter(AndEvents[now_date]),Counter(IosEvents[now_date])
    allEvents[now_date] = {}
    allEvents[now_date] = dict(x+y)

    for k in allEvents[now_date]:
        print(k,allEvents[now_date][k])

    print(IosEvents)
    print(AndEvents)
    print(allEvents)


except aop.ApiError as e:
    # Api网关返回的异常
    print(e)
except aop.AopError as e:
    # 客户端Api网关请求前的异常
    print(e)
except Exception as e:
    # 其它未知异常
    print(e)