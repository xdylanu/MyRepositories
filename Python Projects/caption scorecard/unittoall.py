import os
import csv
folderdir = r"F:\temp\CaptionScoreCard"
for foldername in os.listdir(folderdir):
    subpath = folderdir + "\\" + foldername
    out_path = subpath + '.tsv'
    if os.path.exists(out_path):
        os.remove(out_path)
    first = True
    for filename in os.listdir(subpath):
        head = True
        with open(subpath + '\\' + filename, encoding="utf-8") as tsvin, open(out_path, 'a', encoding="utf-8") as tsvout:
            # tsv_in = csv.reader(tsvin, delimiter='\t')
            # tsv_out = csv.writer(tsvout, delimiter='\t')
            for row in tsvin:
                # print(filename + ':' + str(tsv_in.line_num))
                if head:
                    head = False
                    if not first:
                        continue
                    first = False
                tsvout.write(str(row))


