import os
import csv
folderdir = r"F:\temp"
for foldername in os.listdir(folderdir):
    subpath = folderdir + "\\" + foldername
    out_path = subpath + '.tsv'
    if os.path.exists(out_path):
        os.remove(out_path)
    Body = 0
    BingMobile = 0
    Head = 0
    BingDesktop = 0
    Google = 0
    Tail = 0
    for filename in os.listdir(subpath):
        head_row = True
        with open(subpath + '\\' + filename, encoding="utf-8") as tsvin:
            for row in tsvin:
                if head_row:
                    head_row = False
                    continue
                slist = row.split('\t')
                if slist[0] == "Head":
                    Head +=  int(slist[1].strip('\n'))
                elif slist[0] == "Body":
                    Body +=  int(slist[1].strip('\n')) 
                elif slist[0] == "Tail":
                    Tail +=  int(slist[1].strip('\n'))
                elif slist[0] == "BingMobile":
                    BingMobile +=  int(slist[1].strip('\n'))
                elif slist[0] == "BingDesktop":
                    BingDesktop +=  int(slist[1].strip('\n'))
                elif slist[0] == "Google":
                    Google +=  int(slist[1].strip('\n'))
    with open(out_path, 'a', encoding="utf-8") as tsvout:
        tsvout.write('QCategorie\tQCount\n')
        tsvout.write('%s\t%s\n' % ('Body',Body))
        tsvout.write('%s\t%s\n' % ('BingMobile',BingMobile))
        tsvout.write('%s\t%s\n' % ('Head',Head))
        tsvout.write('%s\t%s\n' % ('BingDesktop',BingDesktop))
        tsvout.write('%s\t%s\n' % ('Google',Google))
        tsvout.write('%s\t%s\n' % ('Tail',Tail))


















