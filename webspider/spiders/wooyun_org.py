#!-*-encoding:utf-8-*-
from scrapy.spiders import Spider
import scrapy
from webspider.items import WooyunItem
from webspider.itemLoaders import WooyunLoader
from scrapy.exceptions import CloseSpider
import datetime
import os 
from os.path import dirname
from webspider.settings import TOP_DIR


class WooyunSpider(Spider):
	"""
	"""
	
	name = "wooyun"
	start_urls = [
		          "http://www.wooyun.org/bugs/page/1",
				  ]
	
	allowed_domains = ["www.wooyun.org"]

	custom_settings={
		'ITEM_PIPELINES':
			{
			'webspider.pipelines.WooyunPipeline': 310,			
			},
		'JOBDIR':os.path.join(TOP_DIR,'wooyun_spider_runtime'),
		 }	

	# max_page_num is used to limit the deepth by the webpage's paginator indicator.
	# so it is pretty acurrate
	# for example,if max_page_num is 10, http://www.wooyun.org/bugs/page/11 are not reacheable.
	max_page_num = 4000

		
	def parse(self,response):
		"""
		"""
		urls = response.xpath("//div[@class='content']/table[@class='listTable']/tbody/tr/td/a/@href").extract()
		for url in urls:

			yield scrapy.Request(response.urljoin(url), callback=self.parse_one)
			
		next_page = response.xpath("//div[@class='content']/p[@class='page']/a[@class='current']/following-sibling::a[1]")
		current_page = response.xpath("//div[@class='content']/p[@class='page']/a[@class='current']")
		current_page_num = int(current_page.xpath("./text()").extract()[0])

		# if not next page ,IndexError will be raise by the system
		if next_page and current_page_num <= self.max_page_num:
			next_page_url = response.urljoin(next_page.xpath("./@href").extract()[0])
			yield scrapy.Request(next_page_url,callback=self.parse)
		#else:
		#	raise CloseSpider("crawled all the pages you need!")
		# Don't try to stop the spider,because other runing start_url may not reach the limitation
		# one can only end self,but not others

					
		
		
		
	def parse_one(self, response):

		bug_item = WooyunLoader(item=WooyunItem(),response=response)
		bug_item.add_xpath("hole_series_num","//div[@class='content']/h3[1]/a/text()")
		bug_item.add_xpath("title","//div[@class='content']/h3[@class='wybug_title']/text()")
		bug_item.add_xpath("related_company","//div[@class='content']/h3[@class='wybug_corp']/a/text()")
		bug_item.add_xpath("author","//div[@class='content']/h3[@class='wybug_author']/a/text()")		
		bug_item.add_xpath("PubTime","//div[@class='content']/h3[@class='wybug_date']/text()")		#提交时间				
		bug_item.add_xpath("public_time","//div[@class='content']/h3[@class='wybug_open_date']/text()")	#公开时间
		bug_item.add_xpath("hole_type","//div[@class='content']/h3[@class='wybug_type']/text()")
		bug_item.add_xpath("damage_level","//div[@class='content']/h3[@class='wybug_level']/text()")	
		bug_item.add_xpath("hole_status","//div[@class='content']/h3[@class='wybug_status']/text()")
		bug_item.add_value("hole_origin",response.url)
		bug_item.add_xpath("tags","/html/body/div[@class='content']/h3[contains(text(),'Tags')]/span/a/text()")            #ok
		bug_item.add_xpath("hole_hash","/html/body/div[@class='content']/h3[@class='detailTitle' and contains(text(),'hash')]/text()")		#ok

		bug_item.add_css("disclose_status","#bugDetail>div.content>p.detail.wybug_open_status::text")
		bug_item.add_css("description","#bugDetail>div.content>p.detail.wybug_description::text")

		bug_item.add_xpath("hole_detail","/html/body/div[@class='content']/div[@class='wybug_detail']")
		bug_item.add_xpath("hole_poc","/html/body/div[@class='content']/div[@class='wybug_poc']")		
		bug_item.add_xpath("hole_patch","/html/body/div[@class='content']/div[@class='wybug_patch']")
		bug_item.add_css("company_reply","#bugDetail>div.content>div.bug_result")

		bug_item.add_xpath("hole_detail_text","/html/body/div[@class='content']/div[@class='wybug_detail']")
		bug_item.add_xpath("hole_poc_text","/html/body/div[@class='content']/div[@class='wybug_poc']")		
		bug_item.add_xpath("hole_patch_text","/html/body/div[@class='content']/div[@class='wybug_patch']")
		bug_item.add_css("company_reply_text","#bugDetail>div.content>div.bug_result")

		bug_item.add_value("saved_time",datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))	
																		
		return bug_item.load_item()


class WooyunUpdator(WooyunSpider):
	"""
		Bugs in wooyun.org mainly go this process:
		-> new_submit   
		-> new_confirm
		-> new_public
		namely, a bug in wooyun.org have 3 states,
		all the bugs which ever the state it is will be place in 
		http://www.wooyun.org/bugs/page/:num
	"""
	name = "wooyun_updator"

	# new_public signify the bug is repired by the company,
	# then the company wooyun.org update the bug status,
	# so wee need to update it.

	# new_confirm signify the company acknowleadge the bug,
	# and the company probably to fix it later.

	# new_submit signify someone just find another new bug

	start_urls = ["http://www.wooyun.org/bugs/new_submit/",
				"http://www.wooyun.org/bugs/new_confirm/",
				"http://www.wooyun.org/bugs/new_public/",				
				"http://www.wooyun.org/bugs/page/1",]

	custom_settings={

		'ITEM_PIPELINES':
			{
				'webspider.pipelines.WooyunPipeline': 310,			
			},
		 }	

	max_page_num = 3