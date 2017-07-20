# coding: utf-8
import threading
import time
import re
import os
import operator
"""
具体含义看文档
功能：获取每一个cpu的利用率.
输入：interval间隔时间，time次数
返回:每一个字典cpu的使用率%
"""
def addCPU(limit):
    while(True):
        st_time = time.time();
        while((time.time()-st_time)<limit):
            pass  
        time.sleep(1-limit)
def addMem(mem):
    temp = []
    while(float(getMemusage())<mem):
        for i in range(int(1024*mem*100)):
            temp.append(i)
    time.sleep(100000)        

def getstatCPU(mininterval=1):
    usage = {}
    while True:       
        name1,total1,idle1 = getstatInfo()
        time.sleep(mininterval)
        name2,total2,idle2 = getstatInfo()
        for i in range(0,len(name1)-1):
            #print(idle2[i]-idle1[i],total2[i]-total1[i])
	    usage[name1[i]]=100-((idle2[i]-idle1[i])/(float)(total2[i]-total1[i]))*100
        print (usage)
    return usage
 
"""
功能获取当前cpu运行状态
"""
def getstatInfo():
    fp = open('/proc/stat')
    num = -1
    temp = 0
    total = []
    idle = []
    name = []
    while fp:
        fpline = fp.readline()
        if fpline =='':
            break;
        fpline = re.split(' |\t|\n',fpline)
        num += 1
        if re.match(r'cpu\d+',fpline[0]):
            temp = 0
	    for i in range(1,10):
                temp += int(fpline[i],10)
            total.append(temp)
            idle.append(int(fpline[4],10))
            name.append(fpline[0])
    fp.close()
    return name,total,idle


"""
功能：获取当前系统内存使用率
"""
def getMemusage():
    MEMSTRING = "free |sed -n '2p' |gawk 'x = ($3/$2){print x}'"
    memusage = os.popen(MEMSTRING)
    return memusage.read()
"""
功能：获取当前硬盘使用率
"""
def getHarddisk():
    DISKSTRING = "df -h /dev/sda1 |sed -n '/% \//p' | gawk '{print $5}'"
    diskusage = os.popen(DISKSTRING)
    return diskusage.read()

"""
功能：获取当前网络使用情况统计值
"""
def getNetwork():
    NETSTRING = "netstat -s"
    netinfo = os.popen(NETSTRING)
    return netinfo.read()
def stopall():
    time.sleep(100)
    print "stopall"
    exit()
def addload(mem,cpu):
    threads = []
    #tmem = threading.Thread(target=addCPU,args=(mem,))
    #threads.append(tmem)
    tcpu = threading.Thread(target=addCPU,args=(cpu,))
    threads.append(tcpu)
    tstop = threading.Thread(target=stopall)
    threads.append(tstop)
    for thread in threads:
        thread.setDaemon(True)
        thread.start()
    thread.join()
import sys
getstatCPU()
#addload(float(sys.argv[1])/100,float(sys.argv[2])/100)
