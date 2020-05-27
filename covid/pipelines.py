# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CovidPipeline(object):
    def process_item(self, item, spider):
        help = str(item['getHelp']).replace("'",'"')
        stats = str(item['covidStats']).replace("'",'"')
        title = item['title'].replace("'", '"')
        f = open("resources/scrapedResults.txt", "w+", encoding='utf8')
        f.write("{\"covidStats\":"+stats+"}\n{\"getHelp\":"+help+"}\n{\"title\":\""+title+"\"}")
        f.close()
        return item


class CovidSymptoms(object):
    def process_item(self, item, spider):
        symptoms = str(item['symptoms']).replace("'",'"')
        title = item['title'].replace("'",'"')
        f = open("resources/covidSymptoms.txt", "w+", encoding='utf8')
        f.write("{\"symptoms\":"+symptoms+"}\n{\"title\":\""+title+"\"}")
        f.close()
        return item
