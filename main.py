from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.utils.log import configure_logging

from covid.settings import ITEM_PIPELINES, BOT_NAME, SPIDER_MODULES
from covid.spiders.covidEE import CovidEESpider


def stop():
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def configureRunner():
    global s
    s = get_project_settings()
    s['ITEM_PIPELINES'] = ITEM_PIPELINES
    s['LOG_LEVEL'] = 'INFO'
    #s['LOG_ENABLED'] = False
    s['BOT_NAME'] = BOT_NAME
    s['SPIDER_MODULES'] = SPIDER_MODULES
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    configure_logging(s)


if __name__ == '__main__':

    # Run the Spiders
    # Read the saved file for info
    # Parse the file
    # Display the output here.

    configureRunner()
    runner = CrawlerRunner(settings=s)
    d = runner.crawl(CovidEESpider)

    try:
        country= input("Enter the country you want information for(done to exit): ")
        if country.lower() == "done":
            raise Exception ("Exit called. ")
        print("Fetching your information . . .")
        file = open("resources/scrapedResults.txt", 'r', encoding='utf8')
        print(file.read())
        file.close()
    except Exception as e:
        print (e)
        stop()
    else:
        stop()
