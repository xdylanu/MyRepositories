import json
import adal
import math
import sys
from urllib import request
from termcolor import colored

scrapings = {}
allResults = {}

def getToken():
    auth_context = adal.AuthenticationContext(authority)
    token = auth_context.acquire_token_with_client_credentials(resource=resource,client_id=client_id,client_secret=client_secret)
    #print(token)
    return token['accessToken']

def gerUri(token,experimentId,taskId):
    request_param={"experimentId":experimentId,"taskId":taskId}
    data = json.dumps(request_param).encode(encoding='utf-8')
    url="https://techhub.ms/api/v2/GetDcgMetricResultBlobDownloadUris"
    headers = {"Authorization": "Bearer {0}".format(token),"Content-Type": "application/json","Claimed-User-Alias":"v-pichen"}
    req = request.Request(url=url,data=data,headers=headers)
    res = request.urlopen(req)
    res = res.read().decode(encoding='utf-8')
    if ("downloadUris" in res):
        downloadUri = json.loads(res)['downloadUris'][0]
        req = request.Request(url=downloadUri,data=None)
        res = request.urlopen(req)
        res = res.read().decode(encoding='utf-8')
        metricResults = json.loads(res)
        return metricResults

def gerAllTasks(token,experimentId):
    request_param={"experimentId":experimentId,"loadAllEntities":False}
    data = json.dumps(request_param).encode(encoding='utf-8')
    url="https://techhub.ms/api/v2/GetAllExperimentTasksOfExperiment"
    headers = {"Authorization": "Bearer {0}".format(token),"Content-Type": "application/json","Claimed-User-Alias":"v-pichen"}
    req = request.Request(url=url,data=data,headers=headers)
    res = request.urlopen(req)
    res = res.read().decode(encoding='utf-8')
    taskList = json.loads(res)['tasks']   
    return taskList

def parseTasks(token,experimentId,taskList):
    metricResults = {}
    for task in taskList:
        if task['functions'][0] == 'PrepareScrapingQuerySet':
            taskId = task['id']
            name = ''
            if 'explicitQuerySet' in task.keys():
                name = task['explicitQuerySet']['name']
            else:
                name = str(task['rollingSetDurationInSeconds']//3600//24) + '-day rolling set'
                
            scrapings[taskId] = name
        
        elif 'computationOptions' in task.keys():
        #elif 'computationOptions' in task.keys() and task['id'] == 'bb0ed176-3c7e-4737-a977-ecfea9a06548':
            querySetPreparationTaskId = task['querySetPreparationTaskId']
            #if len(metricResults) == 0:
            taskId = task['id']
            metricResults = gerUri(token,experimentId,taskId)
            if metricResults != None :
                for metric in task['computationOptions']:
                    identifier = metric['identifier']
                    metricType = metric['metricType'] + '@' + str(metric['depth'])
                    parseMetricResult(metricType,metricResults,identifier,querySetPreparationTaskId)
				
        if 'mismatchRates' in task.keys() and len(task['mismatchRates']) > 1:
            querySetPreparationTaskId = task['querySetPreparationTaskIds'][0]
            oneResults = {}
            if querySetPreparationTaskId in allResults.keys():
                oneResults = allResults[querySetPreparationTaskId]
            oneResults['mismatchRateC'] = task['mismatchRates']['0']
            oneResults['mismatchRateT'] = task['mismatchRates'][str(TreatmentCount)]
            oneResults['ScrapingCountC'] = task['scrapeStatusCounts'][querySetPreparationTaskId]['0']
            oneResults['ScrapingCountT'] = task['scrapeStatusCounts'][querySetPreparationTaskId][str(TreatmentCount)]
            allResults[querySetPreparationTaskId] = oneResults  


'''
def downloadFile(downloadUri,outfile):
    print(downloadUri)
    request.urlretrieve(downloadUri, outfile)
'''


def formatJudgedRate(judgedRate):
    result = ''
    if judgedRate == 1:
        result = '0'
    else:
        result = str(round((math.ceil((1 - judgedRate) * 1000) / 10), 1)) + '%'

    return result

def judgePvalue(pvalue,leftJudgedRate,rightJudgedRate,nonTieQueryCount):
    if ((leftJudgedRate is not None) and (leftJudgedRate < 0.95)) or ((rightJudgedRate is not None) and (rightJudgedRate < 0.95)) or ((nonTieQueryCount is not None) and (nonTieQueryCount < 30)):
        pvalue = 'p hidden'
    return pvalue

        
def parseMetricResult(metricType,metricResults,identifier,querySetPreparationTaskId):
    for metric in metricResults:
        resultKey = ''
        # treatment is default for T1;
        #if (metric['metricComputationOptionIdentifier'] == identifier) and (metric['isEstimated'] == JudgeResult) and (metric['rightParameterIndex'] == TreatmentCount):
        if (metric['metricComputationOptionIdentifier'] == identifier) and (metric['isEstimated'] == JudgeResult) and ('rightParameterIndex' in metric.keys() and metric['rightParameterIndex'] == TreatmentCount):
            if ('marketSegment' in metric.keys()) and (metric['marketSegment'] in ['un-UN','fy20_tier1','=en-US']):
                if ('queryCategories' not in metric.keys()):
                    resultKey = metricType + '_'+ metric['marketSegment']

                elif ('queryCategories' in metric.keys()):
                    if ('isFresh' in metric['queryCategories'].keys()) and (metric['queryCategories']['isFresh'] == 'Fresh'):
                        resultKey = metricType + '_'+ metric['marketSegment'] + '_'+ metric['queryCategories']['isFresh']
                        
                    if ('isDeep' in metric['queryCategories'].keys()) and (metric['queryCategories']['isDeep'] == 'Deep'):
                        resultKey = metricType + '_'+ metric['marketSegment'] + '_'+ metric['queryCategories']['isDeep']
                        
                    if ('isLocal' in metric['queryCategories'].keys()) and (metric['queryCategories']['isLocal'] == 'Local'):
                        resultKey = metricType + '_'+ metric['marketSegment'] + '_'+ metric['queryCategories']['isLocal']

                    if ('isSuperFresh' in metric['queryCategories'].keys()) and (metric['queryCategories']['isSuperFresh'] == 'SuperFresh'):
                        resultKey = metricType + '_'+ metric['marketSegment'] + '_'+ metric['queryCategories']['isSuperFresh']

                    if ('decile' in metric['queryCategories'].keys()) and (metric['queryCategories']['decile'] == 'Body'):
                        resultKey = metricType + '_'+ metric['marketSegment'] + '_'+ metric['queryCategories']['decile']
                        
                score = round((metric['rightCommon']['score']- metric['leftCommon']['score']),2)
                pvalue = metric['pValue']
                nonTieQueryCount = metric['nonTieQueryCount']
                if (pvalue is None) or (pvalue == 'NaN'):
                    pvalue = 'NaN'
                elif pvalue >= 0.0001:
                    pvalue = str(round(pvalue,4))
                else:
                    pvalue = ("%.1e" %pvalue)
                pvalue = 'p=' + pvalue   
                Chole = metric['left']['judgedRate']
                Thole = metric['right']['judgedRate']
                #qcount = str(metric['left']['queryCount'])
                qcount = str(nonTieQueryCount)
                if score > 0:
                    score = '+' + str(score)
                else:
                    score = str(score)

                pvalue = judgePvalue(pvalue,Chole,Thole,nonTieQueryCount)   
                
                if (metric['isEstimated'] == True):
                    #result = score + ', ' + pvalue + ', (Fill holes), ' + qcount
                    result = score + ', ' + pvalue
                    #result = score + ', ' + pvalue + ', (' + formatJudgedRate(Chole) + ', ' + formatJudgedRate(Thole) + '), ' + qcount
                else:
                    result = score + ', ' + pvalue + ', (' + formatJudgedRate(Chole) + ', ' + formatJudgedRate(Thole) + '), ' + qcount    
                
                oneResults = {}
                
                if resultKey != '':
                    #print(resultKey)
                    if querySetPreparationTaskId in allResults.keys():
                        oneResults = allResults[querySetPreparationTaskId]
                    if resultKey not in oneResults.keys():                    
                        oneResults[resultKey] = result
                    allResults[querySetPreparationTaskId] = oneResults
                    
def printResults(allResults):
    for taskId, results in allResults.items():
        if len(results) > 2:
            if taskId in scrapings.keys():
                print(scrapings[taskId])
                
            #print(results.keys())
            print('Scraping')
            for i in results['ScrapingCountC']:
                print('ScrapingCountC_' + i + '=' + str(results['ScrapingCountC'][i]))
            for i in results['ScrapingCountT']:
                print('ScrapingCountT_' + i + '=' + str(results['ScrapingCountT'][i]))
            print('')
            print('Mismatch')
            print('C=' +  '%.2f%%' % (results['mismatchRateC'] * 100))
            print('T=' +  '%.2f%%' % (results['mismatchRateT'] * 100))
            print('')
            print('@1_fy20_tier1')
            print(results['OneDcg@1_fy20_tier1'])
            print(results['QcDcg@1_fy20_tier1'])
            print(results['OneDcg@1_fy20_tier1_Deep'])
            print(results['OneDcg@1_fy20_tier1_Fresh'])
            print(results['OneDcg@1_fy20_tier1_SuperFresh'])
            print(results['OneDcg@1_fy20_tier1_Local'])
            print('@1_en-US')
            
            print(results['OneDcg@1_=en-US'])
            print(results['QcDcg@1_=en-US'])
            
            print(results['OneDcg@1_=en-US_Deep'])
            print(results['OneDcg@1_=en-US_Fresh'])
            print(results['OneDcg@1_=en-US_SuperFresh'])
            print(results['OneDcg@1_=en-US_Local'])
            
            print('@1_UN')
            print(results['OneDcg@1_un-UN'])
            print(results['QcDcg@1_un-UN'])
            print(results['OneDcg@1_un-UN_Deep'])
            print(results['OneDcg@1_un-UN_Fresh'])
            print(results['OneDcg@1_un-UN_SuperFresh'])
            print(results['OneDcg@1_un-UN_Local'])
            print('')
            print('@3_fy20_tier1')
            print(results['OneDcg@3_fy20_tier1'])
            print(results['QcDcg@3_fy20_tier1'])
            print(results['OneDcg@3_fy20_tier1_Deep'])
            print(results['OneDcg@3_fy20_tier1_Fresh'])
            print(results['OneDcg@3_fy20_tier1_SuperFresh'])
            print(results['OneDcg@3_fy20_tier1_Local'])
            print('@3_en-US')
            
            print(results['OneDcg@3_=en-US'])
            print(results['QcDcg@3_=en-US'])
            
            print(results['OneDcg@3_=en-US_Deep'])
            print(results['OneDcg@3_=en-US_Fresh'])
            print(results['OneDcg@3_=en-US_SuperFresh'])
            print(results['OneDcg@3_=en-US_Local'])
            
            print('@3_UN')
            print(results['OneDcg@3_un-UN'])
            print(results['QcDcg@3_un-UN'])
            print(results['OneDcg@3_un-UN_Deep'])
            print(results['OneDcg@3_un-UN_Fresh'])
            print(results['OneDcg@3_un-UN_SuperFresh'])
            print(results['OneDcg@3_un-UN_Local'])
            print('')
    
DEBUG = True
resource = "https://localhost:44300/techhub-webapp"
client_id = 'a75ccd90-f516-4e61-a1b9-057d4595a254'
client_secret = ']0l3=7x7@ixP/B1tZ4Ouu=i2ZBhNmhAH'
authority = 'https://login.microsoftonline.com/microsoft.onmicrosoft.com'

if __name__ == '__main__':
    if DEBUG:
    

    #L2 certified
        experimentId = "c4e23181-2cc2-41c8-8cf5-2724ac27276b"
    #L2W6 rc4
        #experimentId = "e881c192-df8a-4847-8d5a-312a9b44a82d"

    #L2 rc1
        #experimentId = "2a0500a2-2134-4fb2-9500-389efab1222c"
    #L2 rc2
        #experimentId = "ba8a28a5-5cc9-4d3f-9458-ded8e00aaa49"
    #L2 rc3
        #experimentId = "3db9c782-1bdd-4dcb-9137-8fa3a48afe97"
    #L2 rc4
        #experimentId = "c53e292f-ea00-4c7b-a7c6-e4d2a8177b8e"
    #L2 rc5
        #experimentId = "e3d367ec-9cb4-440f-8d87-a9e8b9a86d49"


        #experimentId = "5ea8b4ee-595e-4518-8170-d92b894d06ba"

    else:
        experimentId = sys.argv[1]
    
    # TreatmentCount is for which treatment; 1 is for T1, 2 is for T2 ...
    TreatmentCount = 1
    # JudgeResult is for fully judge method; True is for estimate 
    JudgeResult = True
    
    token = getToken()
    taskList = gerAllTasks(token,experimentId)
    parseTasks(token,experimentId,taskList)
    printResults(allResults)
    print('end')   
    
