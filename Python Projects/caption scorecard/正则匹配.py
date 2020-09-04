import os
import re
import csv
folderdir = r"F:\temp"
out_path = folderdir + "\\fr-FR.tsv" 
out_path2 = folderdir + "\\fr-FR 0.65.tsv" 
for filename in os.listdir(folderdir):
    head = True
    with open(folderdir + '\\' + filename, encoding="utf-8") as tsvin, open(out_path, 'a', encoding="utf-8") as tsvout, open(out_path2, 'a', encoding="utf-8") as tsvout2:
        for row in tsvin:
            if head:
                head = False
                continue
            seach = re.search(r'nqlf_f\$turingunivtriggclfvnext:0\.[0-9]{6}',row, re.M|re.I)
            if seach:
                st, va = seach.group().split(':')
                tsvout.write('%s\t%s\n' % (st,va))
                if float(va) >= 0.65:
                    tsvout2.write('%s\t%s\n' % (st,va))


















