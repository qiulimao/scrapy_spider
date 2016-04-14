#-*-encoding:utf-8-*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join,Compose,Identity
import re
from w3lib.html import remove_tags
import datetime

def strip_blank(str_content):
	#scrapy 将所有爬取到的内容都转换为unicode,而正则处理的str和buff类型
	#所以先将 unicode转换为utf-8.但是处理完成以后，需要返回unicode，方便其他processor使用
	cleaned_string = re.sub(r'\s',"",str_content.encode('utf-8'))
	return cleaned_string.decode('utf-8')
    
def filter_useless(str_content):
    cleaned_string =  re.sub(r"vul-level",u"",str_content.encode('utf-8'))
    return cleaned_string.decode('utf-8')
    
def verify_date(str_content):
    if re.search(r"\d{4}-\d{1,2}-\d{1,2}",str_content.encode('utf-8')):
        return str_content
    else:
        return "NULL"
        #return "1970-01-01"
    
    

class BugLoader(ItemLoader):
    default_output_processor = Join()
    default_input_processor = MapCompose(strip_blank)
    danger_level_in = Compose(TakeFirst(),filter_useless,strip_blank)
    discover_time_in = Compose(TakeFirst(),verify_date,strip_blank)
    commit_time_in = Compose(TakeFirst(),verify_date,strip_blank)
    
