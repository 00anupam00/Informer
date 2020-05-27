# -*- coding: utf-8 -*-
import scrapy

from covid.items import CovidItem
from sources.websites import URL1

class CovidEESpider(scrapy.Spider):
    name = 'covidEE'
    allowed_domains = ['terviseamet.ee']
    start_urls = [URL1]
    custom_settings = {
        'ITEM_PIPELINES': {
            'covid.pipelines.CovidPipeline': 300
        }
    }


    def parse(self, response):
        metricsInfo = list()
        result = dict()
        titleInfo = response.xpath('//h2')[2]
        metricsInfo.append(titleInfo.css('h2 strong::text').get())
        divs = response.css('div.static-simple-2columns')[1]
        divHelp = response.css('div.static-infobox02')

        self.getCovidStats(divs, metricsInfo) # Get covid1-19 related metrics list
        #self.getNotice(divs, result) # Get official notice
        self.getHelp(divHelp[1], result)
        yield self.getItem(metricsInfo, result)

    def getCovidStats(self, divs, info):
        for col in divs.css('p.node-lead-emphasized'):
            label = col.css('strong::text').get()
            if label is None:
                label = col.css('font b::text').get()
            info.append(label)

    def getItem(self, metricsInfo, result):
        result[metricsInfo[1]] = metricsInfo[2]
        result[metricsInfo[3]] = metricsInfo[4]
        result[metricsInfo[5]] = metricsInfo[6]
        result['source'] = URL1
        item = CovidItem()
        item['title'] = metricsInfo[0]
        item['news'] = "In Progress"
        item['getHelp'] = result['getHelp']
        del result['getHelp']
        item['covidStats'] = result
        return item

    def getNotice(self, divs, result):
        result['notice'] = divs.xpath('//p/span/text()').get()

    def getHelp(self, help, result):
        getHelp = dict()
        getHelp['title'] = help.css('div.static-infobox02 h1 strong::text').get()
        getHelp['help'] = list()
        for attr in help.css('div.static-infobox02 p.node-lead-default'):
            delim = attr.css('span.node-text-color-red strong::text').get()
            if delim is None: delim = attr.css('u a::text').get()
            getHelp['help'].append(delim.join(attr.css('p::text').getall()).replace('\xa0',' '))
        result['getHelp'] = getHelp
        return result
