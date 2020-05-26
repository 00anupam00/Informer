import scrapy

from covid.items import CovidSymptomsItem
from sources.websites import URL4


class CovidSymptoms(scrapy.Spider):
    name = 'covidSymptoms'
    allowed_domains = ['terviseamet.ee']
    start_urls = [URL4]
    custom_settings = {
        'ITEM_PIPELINES': {
            'covid.pipelines.CovidSymptoms': 300
        }
    }

    def parse(self, response):
        item = CovidSymptomsItem()
        h2 = response.xpath('//h2')[2]
        item['title'] = h2.css('h2::text').get()
        item['symptoms'] = list()
        for sel in response.xpath('//ul/li')[37:51]:
            item['symptoms'].append(sel.css('li::text').get().rstrip(','))
        yield item
