import psutil
import os

pid = psutil.pids()
for pid in pid:
    p = psutil.Process(pid)
    print("pid-%d,pname-%s" %(pid,p.name()))
    if p.name() == 'EXCEL.EXE':
        os.system('taskkill /f /pid %s' % p.name())
        break

