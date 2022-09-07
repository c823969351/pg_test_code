import requests
import json
import bs4
from requests.models import Response

def get_translate_date(word=None):
    url = "https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    From_data = {"i": word,
    "from" : "AUTO",
    "to": "AUTO",
    "smartresult": "dict",
    "client": "fanyideskweb",
    "salt": "16305756240074",
    "sign": "d337a8642449a2430805425fa565ca3c",
    "lts": "1630575624007",
    "bv":"2bdfc0a89d7fb99f221d3f5a31656471",
    "doctype": "json",
    "version": "2.1",
    "keyfrom" : "fanyi.web",
    "action": "FY_BY_REALTlME"}
    Response = requests.post(url,data= From_data)
    content = json.loads(Response.text)
    print(content)
def get_html(url_data):
    url = url_data
    strhtml = requests.get(url)
    soup = bs4.BeautifulSoup(strhtml.text,'lxml')
    data = soup.select('body > div.jump-top-box')
    print(data)

    for item in data:
        result = {
        'title':item.get_text(),
        'link':item.get('href')
        }
    print(result)
    

if __name__=='__main__':
    #get_translate_date("我爱你")
    get_html("https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8")

    
