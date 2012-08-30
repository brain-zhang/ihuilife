#coding='utf-8'
SANDBOX_TEST = True
if SANDBOX_TEST:
    URL = 'gw.api.tbsandbox.com'
    PORT = 80
    APPKEY = '1021098591'
    APP_SECRECT = 'sandbox5f068ad98a7d39f148ea9a25e'
    PID = 32399943
else:
    URL = 'gw.api.taobao.com'
    PORT = 80
    APPKEY = '21098591'
    APP_SECRECT = '7e440955f068ad98a7d39f148ea9a25e'
    PID = 32399943