# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
	name = 'tencent'
	allowed_domains = ['tencent.com']
	base_url = 'http://hr.tencent.com/position.php?&start='
#    for i in range(218):
#    	url = base_url + '=' + str(i*10)
	offset = 0

	start_urls = [(base_url + str(offset))]

	def parse(self, response):
		urls = response.xpath("//tr[@class='even']" or "//tr[@class='odd']")
		for url in urls:
			positionName = url.xpath('./td[1]/a/text()').extract()[0]
			positionLink = url.xpath('./td[1]/a/@href').extract()[0]

			try:
				positionType = url.xpath('./td[2]/text()').extract()[0]
			except IndexError as e:
				positionType = '没有职位描述'
			#教程上用下面代替上面
			#if len(url.xpath('./td[2]/text()').extract()[0]):
			#    positionType = url.xpath('./td[2]/text()').extract()[0]
			#else:
			#    positionType = ''

			peopleNumber = url.xpath('./td[3]/text()').extract()[0]
			workLocation = url.xpath('./td[4]/text()').extract()[0]
			publishTime = url.xpath('./td[5]/text()').extract()[0]

			item = TencentItem()
			item['positionName'] = positionName
			item['positionLink'] = positionLink
			item['positionType'] = positionType
			item['peopleNumber'] = peopleNumber
			item['workLocation'] = workLocation
			item['publishTime'] = publishTime

			yield item

		if self.offset < 2190:#if response.status_code == 200:这种写法可以吗
			self.offset += 10
			url = self.base_url + str(self.offset)
			yield scrapy.Request(url,callback = self.parse)#回调函数
			#yield scrapy.Request(url,callback = self.parse_next)#回调函数可以不重复上面parse
	#def parse_next(self,response):
	#	pass

		#下面三行能替代上面的if语句，主要作用就是抓取下一页
		#if not len(response.xpath("//a[@class='noactive' and @id='next']")):
		#	url = response.xpath("//a[@id='next']/@href").extract()[0]
		#	yield scrapy.Request('http://hr.tencent.com/' + url,callback = self.parse)