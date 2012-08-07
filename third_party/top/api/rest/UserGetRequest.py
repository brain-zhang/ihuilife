'''
Created by auto_sdk on 2012-08-07 12:41:14
'''
from top.api.base import RestApi
class UserGetRequest(RestApi):
	def __init__(self,domain,port):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.nick = None

	def getapiname(self):
		return 'taobao.user.get'
