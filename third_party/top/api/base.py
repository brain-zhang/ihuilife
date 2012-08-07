# -*- coding: utf-8 -*-
'''
Created on 2012-7-3

@author: lihao
'''
import httplib
import urllib
import time
import hashlib
import json

'''
定义一些系统变量
'''

SYSTEM_GENERATE_VERSION = "taobao-sdk-python-20120807"

P_APPKEY = "app_key"
P_API = "method"
P_SESSION = "session"
P_ACCESS_TOKEN = "access_token"
P_VERSION = "v"
P_FORMAT = "format"
P_TIMESTAMP = "timestamp"
P_SIGN = "sign"
P_SIGN_METHOD = "sign_method"
P_PARTNER_ID = "partner_id"

P_CODE = 'code'
P_SUB_CODE = 'sub_code'
P_MSG = 'msg'
P_SUB_MSG = 'sub_msg'


N_REST = '/router/rest'

def sign(secret, parameters):
    #===========================================================================
    # '''签名方法
    # @param secret: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # '''
    #===========================================================================
    # 如果parameters 是字典类的话
    if hasattr(parameters, "items"):
        keys = parameters.keys()
        keys.sort()
        
        parameters = "%s%s%s" % (secret,
            str().join('%s%s' % (key, parameters[key]) for key in keys),
            secret)
    sign = hashlib.md5(parameters).hexdigest().upper()
    return sign

class TopException(Exception):
    #===========================================================================
    # 业务异常类
    #===========================================================================
    def __init__(self):
        self.errorcode = None
        self.message = None
        self.subcode = None
        self.submsg = None
        self.application_host = None
        self.service_host = None
    
    def __str__(self, *args, **kwargs):
        sb = "errorcode=" + str(self.errorcode) +\
            " message=" + str(self.message) +\
            " subcode=" + str(self.subcode) +\
            " submsg=" + str(self.submsg) +\
            " application_host=" + str(self.application_host) +\
            " service_host=" + str(self.service_host)
        return sb
       
class RequestException(Exception):
    #===========================================================================
    # 请求连接异常类
    #===========================================================================
    pass

class RestApi(object):
    #===========================================================================
    # Rest api的基类
    #===========================================================================
    
    def __init__(self, domain, port = 80):
        #=======================================================================
        # 初始化基类
        # Args @param domain: 请求的域名或者ip
        #      @param port: 请求的端口
        #=======================================================================
        self.__domain = domain
        self.__port = port
        self.__httpmethod = "POST"
        
    def get_request_header(self):
        return {
                 'Content-type': 'application/x-www-form-urlencoded',
                 "Cache-Control": "no-cache",
                 "Connection": "Keep-Alive",
        }
        
    def set_app_info(self, appinfo):
        #=======================================================================
        # 设置请求的app信息
        # @param appinfo: import top
        #                 appinfo top.appinfo(appkey,secret)
        #=======================================================================
        self.__app_key = appinfo.appkey
        self.__secret = appinfo.secret
        
    def getapiname(self):
        return ""
    
    def _check_requst(self):
        pass
    
    def getResponse(self, authrize=None, timeout=30):
        #=======================================================================
        # 获取response结果
        #=======================================================================
        connection = httplib.HTTPConnection(self.__domain, self.__port, timeout)
        sys_parameters = {
            P_FORMAT: 'json',
            P_APPKEY: self.__app_key,
            P_SIGN_METHOD: "md5",
            P_VERSION: '2.0',
            P_TIMESTAMP: str(long(time.time() * 1000)),
            P_PARTNER_ID: SYSTEM_GENERATE_VERSION,
            P_API: self.getapiname(),
        }
        if authrize is not None:
            sys_parameters[P_SESSION] = authrize
        application_parameter = self.getApplicationParameters()
        sign_parameter = sys_parameters.copy()
        sign_parameter.update(application_parameter)
        sys_parameters[P_SIGN] = sign(self.__secret, sign_parameter)
        connection.connect()
        body = urllib.urlencode(application_parameter)
        url = N_REST + "?" + urllib.urlencode(sys_parameters)
        connection.request(self.__httpmethod, url, body=body, headers=self.get_request_header())
        response = connection.getresponse();
        if response.status is not 200:
            raise RequestException('invalid http status ' + str(response.status) + ',detail body:' + response.read())
        result = response.read()
        jsonobj = json.loads(result)
        if jsonobj.has_key("error_response"):
            error = TopException()
            if jsonobj["error_response"].has_key(P_CODE) :
                error.errorcode = jsonobj["error_response"][P_CODE]
            if jsonobj["error_response"].has_key(P_MSG) :
                error.message = jsonobj["error_response"][P_MSG]
            if jsonobj["error_response"].has_key(P_SUB_CODE) :
                error.subcode = jsonobj["error_response"][P_SUB_CODE]
            if jsonobj["error_response"].has_key(P_SUB_MSG) :
                error.submsg = jsonobj["error_response"][P_SUB_MSG]
            error.application_host = response.getheader("Application-Host", "")
            error.service_host = response.getheader("Location-Host", "")
            raise error
        return jsonobj
    
    
    def getApplicationParameters(self):
        application_parameter = {}
        for key, value in self.__dict__.iteritems():
            if not key.startswith("__") and not key.startswith("_RestApi__") and value is not None :
                application_parameter[key] = value
        return application_parameter
    
    
        
