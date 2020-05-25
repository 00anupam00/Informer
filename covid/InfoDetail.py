import requests
from sources.websites import URL3

class Info():
    data = list()

    def __init__(self, countyName='') -> None:
        response = requests.get(URL3)
        data = response.json()
        if len(countyName) > 0:
            for obj in data:
                if obj['County'] == countyName:
                    self.data.append(obj)
        else:
            self.data = data
        super().__init__()

    # cumulative details about the county
    def getCountyDetails(self):
        pass

    # positive tests each day
    def getDailyCovidInfo(self):
        pass

    # Total test conducted in the county.
    def getTotalTestsByCounty(self):
        return len(self.data)

    def getTotalTests(self):
        pass

    def getTotalPositiveCasesByCounty(self):
        result = [ele for ele in self.data if ele['ResultValue'] == 'P']
        return len(result)

    def getTotalPositiveCases(self):
        return len([ele for ele in self.data if ele['ResultValue'] == 'P'])

    def mostAffectedAge(self):
        result = dict()
        for obj in self.data:
            if obj['AgeGroup'] in result:
                result[obj['AgeGroup']] += 1
            else:
                result[obj['AgeGroup']] = 1
        result_sort = sorted(result.items(), key=lambda x: x[1], reverse = True)
        return next(iter(result_sort))

    def posCasesPerDayByCounty(self):
        result = dict()
        for attr in self.data:
            if attr['StatisticsDate'] in result.keys():
                result[attr['StatisticsDate']].append(attr['ResultValue'])
            else:
                result[attr['StatisticsDate']] = list(attr['ResultValue'])
        return [v.count('P') for k,v in result.items()]