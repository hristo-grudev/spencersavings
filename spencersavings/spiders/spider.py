import scrapy

from scrapy.loader import ItemLoader

from ..items import SpencersavingsItem
from itemloaders.processors import TakeFirst


class SpencersavingsSpider(scrapy.Spider):
	name = 'spencersavings'
	start_urls = ['https://www.spencersavings.com/category/spencer-news/']

	def parse(self, response):
		post_links = response.xpath('//h2[@class="entry-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="wrapper page_headline "]//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=SpencersavingsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
