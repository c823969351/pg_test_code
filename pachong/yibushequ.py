import requests
from pyquery import PyQuery as pq
import os,sys
from bs4 import BeautifulSoup
os.chdir('D:\TestCode\pachong')

def crawle():   
    url='https://www.epubit.com/pubcloud/content/front/getContentsByFolderId?folderId=0e28da26-c19c-4c4a-be4b-c28abd435780&projectId=ca897088-fead-4d07-ba1f-874aab2bbacd&src=normal'    
    req=requests.get(url=url)
    req.encoding = req.apparent_encoding
    html=req.text

    soup = BeautifulSoup(html,'html.parser')
    for a in soup.p.strings:
        print(a)
    # for child in soup.body.children:
    #     print(child)
    text = soup.select('p')
    print(text)






if __name__ == '__main__':
    crawle()
    #url='https://www.777zw.net/1/1429/927130.html'
    #Text(url)