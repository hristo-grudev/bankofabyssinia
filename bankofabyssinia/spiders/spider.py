import scrapy

from scrapy.loader import ItemLoader

from ..items import BankofabyssiniaItem
from itemloaders.processors import TakeFirst


class BankofabyssiniaSpider(scrapy.Spider):
	name = 'bankofabyssinia'
	start_urls = ['https://www.bankofabyssinia.com/news/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="cmsmasters_post_read_more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="cmsmasters_post_content entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//abbr[@class="published"]/text()').get()

		item = ItemLoader(item=BankofabyssiniaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
