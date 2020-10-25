import aop
import aop.api
import json

# 设置网关域名
aop.set_default_server('gateway.open.umeng.com')

# 设置apiKey和apiSecurity
aop.set_default_appinfo(1046050, "0HKvp0jGmlp")

# 构造Request和访问协议是否是https
req = aop.api.UmengUappGetAllAppDataRequest()

# 发起Api请求
try:
    resp = req.get_response(None)
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