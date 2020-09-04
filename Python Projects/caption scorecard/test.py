import os
import csv
folderdir = r"F:\temp"
for foldername in os.listdir(folderdir):
    subpath = folderdir + "\\" + foldername
    out_path = subpath + '.tsv'
    if os.path.exists(out_path):
        os.remove(out_path)
    for filename in os.listdir(subpath):
        count = 0
        time = ''
        day = 0
        hour = 0
        minute = 0
        second = 0
        with open(subpath + '\\' + filename, encoding="utf-8") as tsvin:
            for row in tsvin:
                slist = row.strip('\n').split('\t')
                count += int(slist[1].split('/')[0])
                time = slist[2].split(' ')
                for s in time:
                    s = s.strip('(').strip(')')
                    if s.endswith('h'):
                        hour += int(s.strip('h'))
                    elif s.endswith('d'):
                        day += int(s.strip('d'))
                    elif s.endswith('m'):
                        minute += int(s.strip('m'))
                    elif s.endswith('s'):
                        second += int(s.strip('s'))
                a = 0
        minute += second // 60
        second = second % 60
        hour += minute // 60
        minute = minute % 60
        day += hour // 24
        hour = hour % 24
        with open(out_path, 'a', encoding="utf-8") as tsvout:
            tsvout.write('%s\t%s\t%s\n' % (filename.split('.')[0],count,str(day) + 'd ' + str(hour) + 'h ' + str(minute) + 'm ' + str(second) + 's'))


















