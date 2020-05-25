from time import sleep

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.utils.log import configure_logging

from covid.settings import ITEM_PIPELINES, BOT_NAME, SPIDER_MODULES
from covid.spiders.covidEE import CovidEESpider

from  covid.InfoDetail import Info
import matplotlib.pyplot as plt
import pprint


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
    result = dict()

    infoByCounty = Info(countyName)
    totalInfo = Info()

    totalPosCasesInCounty = infoByCounty.getTotalPositiveCasesByCounty() # Total no. of positive cases
    totalTestsInCounty = infoByCounty.getTotalTestsByCounty()# Total tests conducted in the county
    totalPosCases = totalInfo.getTotalPositiveCases()

    result['Total Number of positive cases in your County'] = totalPosCasesInCounty
    result['Total tests conducted in your County'] = totalTestsInCounty

    # If more detailed information required. Provide some graphs and comparisons.
    if 'Y' == detailedInfo:
        # Total percentage of positive cases of county against positive cases in country
        posCasesAgainstCountryPer = totalPosCasesInCounty * 100 / totalPosCases

        # Percentage of positive cases against total tests done in the county.
        positiveCaseByTestPer = totalPosCasesInCounty * 100 / totalTestsInCounty

        # Mostly affected age-group in your county
        mostAff = infoByCounty.mostAffectedAge()

        result['Positive tests percentage in you County'] = str(round(positiveCaseByTestPer,2)) + "%"
        result['Percentage of positive cases in your County by Country Avg.'] = str(
            round(posCasesAgainstCountryPer, 2)) + "%"
        result['Most Affected groups are from range '] = mostAff

        posCasesPerDay = infoByCounty.posCasesPerDayByCounty()
        plt.plot(posCasesPerDay)
        plt.ylabel("No. of positive cases per day in your county.")
        plt.show()

    return result


def emergencyInfoByCounty(county):
    # Get helpline number by county.
    pass


def getSymptoms():
    # Covid-29 known symptoms
    pass


def checkExit(inp):
    if inp.lower() == 'done' or inp.lower() == 'exit' or inp.lower() == 'quit':
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
        print("Welcome to the Covid-Informer App.")
        sleep(1)
        print("Fetching initial information of Estonia ...")
        sleep(3)
        file = open("resources/scrapedResults.txt", 'r', encoding='utf8')
        print(file.read())  # Provide an elegant result from the file.
        file.close()
        while True:
            print("Follow the instructions to get latest updates and more info on Covid-19 relevant to you county")
            print("Or, Enter done/exit/quit to exit the application anytime!")
            sleep(2)
            county = input("Enter the county you want covid-19 information for: ")
            print(pprint.pformat(countyInfo(county, 'N'), indent=1, width=80))  # Fetch the county info from the Govt. provided api.
            checkExit(county)

            detailedInfo = input("Do you want more detailed covid-19 info of the particular county? [Y/N] ")
            if detailedInfo.lower() == 'y':
                print(pprint.pformat(countyInfo(county, 'Y'), indent=1, width=80))
            else:
                checkExit(detailedInfo)

            symptoms = input("Would you like to know the symptoms for Covid-19? [Y/N] ")
            if symptoms.lower() == 'y':
                getSymptoms()
            else:
                checkExit(symptoms)

            emergencyHelp = input("Would you like to get the emergency contact of your county [Y/N] ")
            if emergencyHelp.lower() == 'y':
                emergencyInfoByCounty(county)
            else:
                checkExit(emergencyHelp)
            sleep(1)
            print("Let's continue with another county info ...")
            sleep(3)
    except Exception as e:
        print(e)
        stop()
    else:
        stop()
