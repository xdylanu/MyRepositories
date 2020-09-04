import os
import sys
import json
import adal
import math
import shutil
from urllib import request
from termcolor import colored

scrapings = {}
allResults = {}

def getToken():
    auth_context = adal.AuthenticationContext(authority)
    token = auth_context.acquire_token_with_client_credentials(resource=resource,client_id=client_id,client_secret=client_secret)
    return token['accessToken']

def gerUri(token,experimentId,taskId):
    request_param={"experimentId":experimentId,"taskId":taskId}
    data = json.dumps(request_param).encode(encoding='utf-8')
    url="https://techhub.ms/api/v2/GetDcgMetricResultBlobDownloadUris"
    headers = {"Authorization": "Bearer {0}".format(token),"Content-Type": "application/json","Claimed-User-Alias":"v-pichen"}
    req = request.Request(url=url,data=data,headers=headers)
    res = request.urlopen(req)
    res = res.read().decode(encoding='utf-8')
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
    headers = {"Authorization": "Bearer {0}".format(token),"Content-Type": "application/json","Claimed-User-Alias":"v-dyxu"}
    req = request.Request(url=url,data=data,headers=headers)
    res = request.urlopen(req)
    res = res.read().decode(encoding='utf-8')
    taskList = json.loads(res)['tasks']   
    return taskList

def parseTasks(token,experimentId,taskList,marketList):
    metricResults = {}
    for task in taskList:
        if 'computationOptions' in task.keys() and task['functions'][0] == 'ComputeDcgMetrics':
            taskId = task['id']
            metricResults = gerUri(token,experimentId,taskId)
            for metric in task['computationOptions']:
                identifier = metric['identifier']
                metricType = metric['metricType'] + '@' + str(metric['depth'])
                parseMetricResult(metricType,metricResults,identifier,taskId,marketList)
        
def parseMetricResult(metricType,metricResults,identifier,TaskId,marketList):
    for metric in metricResults:
        if (metric['metricComputationOptionIdentifier'] == identifier and metric['isEstimated'] == False):
            # if ('marketSegment' in metric.keys()):
            #     print(metric['marketSegment'])
            # if ('market' in metric.keys()):
            #     print(metric['market'])
            if 'market' in metric.keys() and metric['market'] in marketList:
                if 'queryCategories' in metric.keys():
                    if ('decile' in metric['queryCategories'].keys()) and (metric['queryCategories']['decile'] == 'Head'):
                        downloadFile(TaskId,metric['market'],metric['queryCategories']['decile'],str(metric['left']['queryCount']))                       
                    if ('decile' in metric['queryCategories'].keys()) and (metric['queryCategories']['decile'] == 'Body'):
                        downloadFile(TaskId,metric['market'],metric['queryCategories']['decile'],str(metric['left']['queryCount']))
                    if ('decile' in metric['queryCategories'].keys()) and (metric['queryCategories']['decile'] == 'Tail'):
                        downloadFile(TaskId,metric['market'],metric['queryCategories']['decile'],str(metric['left']['queryCount']))
                    if ('source' in metric['queryCategories'].keys()) and (metric['queryCategories']['source'] == 'BingDesktop'):
                        downloadFile(TaskId,metric['market'],metric['queryCategories']['source'],str(metric['left']['queryCount']))
                    if ('source' in metric['queryCategories'].keys()) and (metric['queryCategories']['source'] == 'BingMobile'):
                        downloadFile(TaskId,metric['market'],metric['queryCategories']['source'],str(metric['left']['queryCount']))
                    if ('source' in metric['queryCategories'].keys()) and (metric['queryCategories']['source'] == 'Google'):
                        downloadFile(TaskId,metric['market'],metric['queryCategories']['source'],str(metric['left']['queryCount']))

def downloadFile(Taskid, market, name, count):
    taskpath = rootpath + '/' + Taskid
    outname = rootpath + '/' + getpathname(Taskid, market) + '.tsv' 
    if not os.path.exists(outname):
        with open(outname, 'a', encoding="utf-8") as tsvout:
            tsvout.write('QCategorie\tQCount\n')
    with open(outname, 'a', encoding="utf-8") as tsvout:
        tsvout.write('%s\t%s\n' % (name, count))

def getpathname(Taskid, market):
    build = {
    #         '2642d141-6660-4e1e-90a7-e9ab2f56f2b5':'2019-10',
    #         '2c984a97-57c7-49d7-9f0e-7796582ac7b2':'2019-09',
    #         'dd467a3a-408d-49eb-a640-e66a23dab5ef':'2019-07',
    #         '4cf5bf86-5c19-4eea-ac0b-eacf1cd6aace':'2019-08',
    #         '1f4d2428-bdff-4037-82e3-24283f7bd168':'2019-12',
    #         '48271d09-66e7-4bef-916c-ca0f823d3cda':'2019-11',
    #         '08aab2ed-d288-4280-9cf6-7eedd8c41804':'2020-02',
    #         'e7a81dc7-3a3d-4f8f-8bd5-fe5f5dbdcacb':'2020-01',
    #         '2561886a-d062-45b1-8353-700d33ab3f2e':'2020-03',
    #         '6afe7651-efe9-4a5b-9f67-dd364e9f3fa7':'2020-04',
    #         'c4096646-b8f2-4faf-a4f0-51815014c4c8':'2020-05',
            # 'a6023a6e-8877-4d4d-adc3-67c849be4ae5':'2020-06',
            'bcd47c4a-6288-4ce5-8f74-6451cdcb020b':'2020-07'}
    return 'QCONT_' + build[Taskid]+ '_' + market
    

if __name__ == '__main__':
    resource = "https://localhost:44300/techhub-webapp"
    client_id = 'a75ccd90-f516-4e61-a1b9-057d4595a254'
    client_secret = ']0l3=7x7@ixP/B1tZ4Ouu=i2ZBhNmhAH'
    authority = 'https://login.microsoftonline.com/microsoft.onmicrosoft.com'
    experimentId = "99c0b699-31e8-4eee-a04f-b8e1d6326e21"
    rootpath = r'F:\temp\techhub'
    if os.path.exists(rootpath):
        shutil.rmtree(rootpath)
    os.mkdir(rootpath)
    marketList = ['de-DE','en-AU','en-CA','en-GB','en-IN','en-US','fr-FR','ja-JP','zh-HK','zh-TW']
    token = getToken()
    taskList = gerAllTasks(token,experimentId)
    parseTasks(token,experimentId,taskList,marketList)
    print('end')   
    

