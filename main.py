from time import sleep

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
    s['LOG_ENABLED'] = False
    s['BOT_NAME'] = BOT_NAME
    s['SPIDER_MODULES'] = SPIDER_MODULES
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    configure_logging(s)


def countyInfo(countyName, detailedInfo):
    # provide county information

    # If more detailed infor required. Provide some graphs and comparisions.
    pass


def emergencyInfoByCounty(county):
    pass


def getSymptoms():
    pass


def checkExit(inp):
    if inp.lower() == 'done':
        sleep(1)
        print()
        print()
        raise ValueError("Thank you for using the Covid-app. Stay Safe!")


if __name__ == '__main__':

    # Run the Spiders
    # Read the saved file for info
    # Parse the file
    # Display the output here.

    configureRunner()
    runner = CrawlerRunner(settings=s)
    d = runner.crawl(CovidEESpider)

    try:
        print("Fetching initial information of Estonia ...")
        sleep(3)
        file = open("resources/scrapedResults.txt", 'r', encoding='utf8')
        print(file.read())  # Provide an elegant result from the file.
        file.close()
        while True:
            county = input("Enter the county you want covid-19 information for(done to exit): ")
            countyInfo(county, 'N')  # Fetch the county info from the Govt. provided api.
            checkExit(county)

            detailedInfo = input("Do you want more detailed covid-19 info of the particular county? [Y/N]")
            if detailedInfo.lower() == 'y':
                countyInfo(county, 'Y')
            else:
                checkExit(detailedInfo)

            symptoms = input("Would you like to know the symptoms for Covid-19? [Y/N]")
            if symptoms.lower() == 'y':
                getSymptoms()
            else:
                checkExit(symptoms)

            emergencyHelp = input("Would you like to get the emergency contact of your county [Y/N]")
            if emergencyHelp.lower() == 'y':
                emergencyInfoByCounty(county)
            else:
                checkExit(emergencyHelp)
            sleep(2)
            print("Let's continue with another county info ...")
            sleep(3)
    except Exception as e:
        print(e)
        stop()
    else:
        stop()
