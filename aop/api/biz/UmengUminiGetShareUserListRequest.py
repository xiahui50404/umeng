# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class UmengUminiGetShareUserListRequest(BaseApi):
    """获取分享用户列表

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.umeng.umini&n=umeng.umini.getShareUserList&v=1&cat=default

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.dataSourceId = None
        self.timeUnit = None
        self.fromDate = None
        self.toDate = None
        self.orderBy = None
        self.direction = None
        self.pageIndex = None
        self.pageSize = None

    def get_api_uri(self):
        return '1/com.umeng.umini/umeng.umini.getShareUserList'

    def get_required_params(self):
        return ['dataSourceId', 'timeUnit', 'fromDate', 'toDate']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return True

    def is_inner_api(self):
        return False
