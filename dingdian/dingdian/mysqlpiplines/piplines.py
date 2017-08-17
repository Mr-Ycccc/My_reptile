from .sql import sql
from dingdian.items import DingdianItem
import sys
import importlib
importlib.reload(sys)


class DingdianPipeline(object):

	def process_item(self,item,spider):
		if isinstance(item,DingdianItem):
			name_id=item['name_id'].encode('utf-8')
			ret=sql.select_name(name_id)
			if ret[0]==1:
				print('已经存在！')
				pass
			else:
				xs_name=item['name'].encode('utf-8')
				xs_author=item['author'].encode('utf-8')
				category=item['category'].encode('utf-8')
				novelurl=item['novelurl'].encode('utf-8')
				serialstatus=item['serialstatus'].encode('utf-8')
				serialnumber=item['serialnumber'].encode('utf-8')
				sql.insert_dd_name(xs_name,xs_author,category,name_id,novelurl,serialstatus,serialnumber)
				print('开始保存：',name_id)