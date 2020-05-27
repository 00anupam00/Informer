from time import sleep

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.utils.log import configure_logging

from covid.settings import BOT_NAME, SPIDER_MODULES
from covid.spiders.CovidSymptoms import CovidSymptoms
from covid.spiders.covidEE import CovidEESpider

from utils.InfoDetail import Info
import matplotlib.pyplot as plt
import pprint
import json
import unicodedata


def configureRunner():
    global s
    s = get_project_settings()
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
        result['Most Affected groups are from range '] = mostAff[0]
        result['Number of positive cases for that group range '] = mostAff[1]

        posCasesPerDay = infoByCounty.posCasesPerDayByCounty()
        plt.plot(posCasesPerDay)
        plt.ylabel("No. of positive cases per day in your county.")
        plt.show()

    return result


def getSymptoms():
    # Covid-29 known symptoms
    file = open("resources/covidSymptoms.txt", 'r', encoding='utf8')
    eestiSymp = dict()
    for line in file:
        eestiSymp.update(json.loads(line))
    file.close()
    print(eestiSymp['title'])
    plog(eestiSymp['symptoms'])


def checkExit(inp):
    if inp.lower() == 'done' or inp.lower() == 'exit' or inp.lower() == 'quit':
        sleep(1)
        print()
        raise ValueError("Thank you for using the Covid-app. Stay Safe!")


def interact():
    try:
        print("Welcome to the Covid-Informer App!")
        sleep(1)
        print("Fetching info ...")
        print()
        sleep(2)
        file = open("resources/scrapedResults.txt", 'r', encoding='utf8')
        eestiInfo = dict()
        for line in file:
            eestiInfo.update(json.loads(line))
        file.close()
        print(eestiInfo['title'])
        plog(eestiInfo['covidStats'])

        print("Follow the instructions to get latest updates and more info on Covid-19 relevant to your county")
        print("Or, Enter done/exit/quit to exit the application anytime!")
        print()
        while True:
            sleep(1)
            county = input("Enter the county you want covid-19 information for: ")
            checkExit(county)
            plog(countyInfo(county, 'N'))

            detailedInfo = input("Do you want more detailed covid-19 info of the particular county? [Y/N]: ")
            if detailedInfo.lower() == 'y':
                plog(countyInfo(county, 'Y'))
            else:
                checkExit(detailedInfo)

            symptoms = input("Would you like to know the symptoms for Covid-19? [Y/N]: ")
            if symptoms.lower() == 'y':
                getSymptoms()
            else:
                checkExit(symptoms)
            emergencyHelp = input("Would you like to get the emergency contact [Y/N]: ")
            if emergencyHelp.lower() == 'y':
                helpData = eestiInfo['getHelp']
                print(helpData['title'])
                plog(helpData['help'])
            else:
                checkExit(emergencyHelp)
            sleep(1)
            print("Let's continue with another county info ...")
            sleep(3)
    except Exception as e:
        print(e)


def plog(object):
    if isinstance(object, dict):
        for k,v in object.items():
            print(k +" : "+ str(v))
    elif isinstance(object, list):
        print(",\n".join(object))
    print()


if __name__ == '__main__':

    # Run the Spiders
    # Read the saved file for info
    # Parse the file
    # Display the output here.

    configureRunner()
    runner = CrawlerRunner(settings=s)
    runner.crawl(CovidEESpider)
    runner.crawl(CovidSymptoms)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


    # Interact with the user
    interact()
