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
    
def remove_colon(str_content):
    #道理同strip_black，处理：时，附带将字符串头尾的空白去除【因为不要无故去除字符串中间的空格】
    cleaned_string =  re.sub(r'^.*：\s*|\s+$',"",str_content.encode('utf-8'))
    return cleaned_string.decode('utf-8')
    
    
def strip_blank_more_than2(str_content):
    cleaned_string = re.sub(r'\s+'," ",str_content.encode('utf-8'))
    return cleaned_string.decode('utf-8')   

def limit_length(str_content):
    cleaned_string = str_content[0:170]
    return cleaned_string      



class SeeBugLoader(ItemLoader):
    """ this itemloader is used for www.seebug.org """

    default_output_processor = Join()
    default_input_processor = MapCompose(strip_blank)
    danger_level_in = Compose(TakeFirst(),filter_useless,strip_blank)
    discover_time_in = Compose(TakeFirst(),verify_date,strip_blank)
    commit_time_in = Compose(TakeFirst(),verify_date,strip_blank)
    
   

class WooyunLoader(ItemLoader):
    """ this itemloader is used for www.wooyun.org """
    
    default_output_processor = Join()
    default_input_processor = MapCompose(strip_blank)
    #原始数据就去除左右两边的空格
    
    #需要去除冒号以前的text
    title_in = Compose(TakeFirst(),remove_colon)
    PubTime_in = Compose(TakeFirst(),remove_colon)
    public_time_in = Compose(TakeFirst(),remove_colon)
    hole_type_in = Compose(TakeFirst(),remove_colon)
    damage_level_in = Compose(TakeFirst(),remove_colon)
    hole_status_in = Compose(TakeFirst(),remove_colon)
    hole_hash_in = Compose(TakeFirst(),remove_colon)
    
    saved_time_in = Identity()
    
    #以下这些字段 还是去除空格吧
    disclose_status_in = MapCompose(strip_blank_more_than2,)
    #漏洞披露状态
    description_in =  MapCompose(strip_blank,)
    #漏洞描述
    hole_detail_in = MapCompose(strip_blank_more_than2,)
    #漏洞详情
    hole_poc_in =  MapCompose(strip_blank_more_than2,)
    #漏洞证明
    hole_patch_in =  MapCompose(strip_blank_more_than2,)
    #漏洞补丁
    company_reply_in =  MapCompose(strip_blank_more_than2,)
    
    description_out=Compose(Join(),limit_length,)
    #厂商回应
    
    hole_detail_text_in = MapCompose(strip_blank_more_than2,remove_tags)
    #漏洞详情
    hole_poc_text_in =  MapCompose(strip_blank_more_than2,remove_tags)
    #漏洞证明
    hole_patch_text_in =  MapCompose(strip_blank_more_than2,remove_tags)
    #漏洞补丁
    company_reply_text_in =  MapCompose(strip_blank_more_than2,remove_tags) 