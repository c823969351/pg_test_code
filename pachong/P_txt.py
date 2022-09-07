import requests
from pyquery import PyQuery as pq
import os,sys
os.chdir('D:\TestCode\pachong')

def crawle():   
    url='https://www.777zw.net/1/1429/'    
    req=requests.get(url=url)
    req.encoding = req.apparent_encoding
    html=req.text

    doc = pq(html)
    a = doc('#list > dl > dd > a')
    m= len(a)
    fr = open('凡人修仙传.txt','w')
    index = 1
    for each in a.items():
        title=each.text()
        url= each.attr('href')
        if url:
            index+=1
            url = 'https://www.777zw.net/1/1429/' + url
            text=Text(url)
            fr.write(title)
            fr.write('\n\n')
            fr.write(text)
            fr.write('\n\n')
            sys.stdout.write('已下载：%.3f%%'%float(index/m)+'\r')
            sys.stdout.flush()

def Text(url):
    #print("正在提取:",url)
    req = requests.get(url=url)
    req.encoding = req.apparent_encoding
    html = req.text
    doc = pq(html)
    item = doc("#content").text()
    return item


if __name__ == '__main__':
    crawle()
    #url='https://www.777zw.net/1/1429/927130.html'
    #Text(url)