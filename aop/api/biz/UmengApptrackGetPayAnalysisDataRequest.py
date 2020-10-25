# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengApptrackGetPayAnalysisDataRequest(BaseApi):
    """根据计划id或单元id查询出该计划id或单元id下用户拍下订单数据

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.apptrack&n=umeng.apptrack.getPayAnalysisData&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.planId = None
        self.unitId = None
        self.queryDate = None
        self.pageNum = None
        self.pageSize = None

    def get_api_uri(self):
        return '1/com.umeng.apptrack/umeng.apptrack.getPayAnalysisData'

    def get_required_params(self):
        return ['planId', 'queryDate']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return False

    def is_inner_api(self):
        return False
