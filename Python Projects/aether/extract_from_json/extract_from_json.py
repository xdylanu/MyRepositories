#-*- coding:utf-8 -*-
import sys
import json
import copy
import re

class phraseclass:
    def __init__(self, market, in_path, out_path):
        lines = self.getFileData(in_path)
        resultList = self.phraseFun(market, lines)
        if resultList:
            self.writerFun(out_path, resultList)
    
    def getFileData(self,in_path):
        with open(in_path,'rb') as load_f:
            lines = load_f.readlines()
        return lines

    def phraseFun(self, market, lines):
        resultList = list()
        for line in lines:
            resultDict = dict()
            dicts = json.loads(line.decode("utf-8"))
            if dicts["market"] == market:
                resultDict["text"] = dicts["text"] if "text" in dicts else ""
                resultDict["market"] = dicts["market"] if "market" in dicts else ""
                results = dicts["algoResults"] if "algoResults" in dicts else ""
                if results:
                    for result in results:
                        resultDict["url"] = result["url"] if "url" in result else ""
                        resultDict["title"] = result["title"] if "title" in result else ""
                        resultDict["snippet"] = result["snippet"] if "snippet" in result else ""
                        resultDict["position"] = result["position"] if "position" in result else ""
                        resultDict["displayUrl"] = result["url"] if "url" in result else ""
                        resultList.append(copy.deepcopy(resultDict))
                else:
                    resultDict["url"] = ""
                    resultDict["title"] = ""
                    resultDict["snippet"] = ""
                    resultDict["position"] = ""
                    resultDict["displayUrl"] = ""
                    resultList.append(copy.deepcopy(resultDict))
        return resultList

    def writerFun(self, out_path, resultList):
        with open(out_path, 'wb') as tsvout: 
            tsvout.write(("query\tmarket\turl\tdisplayUrl\ttitle\tSnippet\tposition\n").encode("utf-8"))
            for result in resultList:
                tsvout.write((re.sub(r"\[(Lat:|Long:|Town:|PostCode:).*?\]", "", result["text"]) + "\t" + result["market"] + "\t" + result["url"] + "\t" + result["displayUrl"] + "\t" + result["title"] + "\t" + result["snippet"] + "\t" + str(result["position"]) + "\n").encode("utf-8"))
            

if __name__ == "__main__":
    # in_path= r"F:/temp/1.json"
    # out_path = r"F:/temp/test.tsv"
    # market = "ru-RU" 
    market = sys.argv[1]
    in_path = sys.argv[2]
    out_path = sys.argv[3]
    phraseclass(market, in_path, out_path)
    
    