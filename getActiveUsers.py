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
req = aop.api.UmengUappGetActiveUsersRequest()

# 发起Api请求
try:
    now_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')

    resp = req.get_response(None, appkey="5c76338bb465f50bc6001045", startDate=start_date, endDate=now_date, periodType="daily")

    #创建字典
    iosDAU = {}
    andDAU = {}
    allDAU = {}

    for k in resp['activeUserInfo']:
        iosDAU[k['date']] = k['value']

    resp2 = req.get_response(None, appkey="5c73a5e9f1f55699ab0000ef", startDate=start_date, endDate=now_date, periodType="daily")

    #Android DAU
    for k in resp2['activeUserInfo']:
        andDAU[k['date']] = k['value']

    x,y = Counter(iosDAU),Counter(andDAU)
    allDAU = dict(x+y)

except aop.ApiError as e:
    # Api网关返回的异常
    print(e)
except aop.AopError as e:
    # 客户端Api网关请求前的异常
    print(e)
except Exception as e:
    # 其它未知异常
    print(e)