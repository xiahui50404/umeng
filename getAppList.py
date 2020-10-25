import aop
import aop.api
import json


#'电竞APP-ios', 'appkey': '5c76338bb465f50bc6001045'
#'电竞APP', 'appkey': '5c73a5e9f1f55699ab0000ef'


# 设置网关域名
aop.set_default_server('gateway.open.umeng.com')

# 设置apiKey和apiSecurity
aop.set_default_appinfo(1046050, "0HKvp0jGmlp")

# 构造Request和访问协议是否是https
req = aop.api.UmengUappGetAppListRequest()

# 发起Api请求
try:
    resp = req.get_response(None, page=1, perPage=10, accessToken="")
    print(resp)
except aop.ApiError as e:
    # Api网关返回的异常
    print(e)
except aop.AopError as e:
    # 客户端Api网关请求前的异常
    print(e)
except Exception as e:
    # 其它未知异常
    print(e)