import os
import csv
folderdir = r"F:\caption scorecard\new all"
for foldername in os.listdir(folderdir):
    subpath = folderdir + "\\" + foldername
    for filename in os.listdir(subpath):
        out_path = folderdir + "\\" + filename
        if os.path.exists(out_path):
            os.remove(out_path)
        head = True
        Market = filename.split('_')[3]
        with open(subpath + '\\' + filename, encoding="utf-8") as tsvin, open(out_path, 'a', encoding="utf-8") as tsvout:
            for row in tsvin:
                if head:
                    head = False
                    tsvout.write('Market\tQuery\tPosition\tTitle\tURL\tDisplayURL\tSnippet\tFirstSubResultType\tSerpUrl\tURLInfoBackendBlob\n')
                else:
                    tsvout.write('%s\t%s' % (Market,str(row)))



















