'''
Created by auto_sdk on 2012-08-07 12:41:14
'''
from top.api.base import RestApi
class ItemGetRequest(RestApi):
	def __init__(self,domain,port):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.num_iid = None
		self.track_iid = None

	def getapiname(self):
		return 'taobao.item.get'
