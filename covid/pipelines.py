# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CovidPipeline(object):
    def process_item(self, item, spider):
        f = open("resources/scrapedResults.txt", "w+", encoding='utf8')
        f.write(str(item))
        f.close()
        # print("Scraped info dumped to resources!!")
        return item
