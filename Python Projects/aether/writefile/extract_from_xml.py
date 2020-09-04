#-*- coding:utf-8 -*-
import time
import sys

class writerclass:
    def __init__(self, out_path):
        self.writerfun(out_path)

    def writerfun(self, out_path):
        newtime = time.strftime("%Y-%m-%d", time.localtime())
        with open(out_path + newtime + '.tsv', 'w') as tsvout: 
            tsvout.write('%s\n%s' % ('BuildVersion', newtime))
            

if __name__ == "__main__":
    # out_path = r"F:/temp/"; 
    out_path = sys.argv[1]
    writerclass(out_path)
    
    