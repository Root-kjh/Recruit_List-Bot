import requests
from urllib import parse
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
driver_path_test="C:\bot-sw\chromedriver.exe"
driver_path_server="/sw/bot-sw/chromedriver"
driver=webdriver.Chrome(driver_path_test,chrome_options=options)

company_count=800
headers = {'User-Agent': 'Mozilla/5.0'}

post_data={'al_eopjong_gbcd':'11111','eopjong_gbcd_list':'11111','eopjong_gbcd':'1','eopjong_cd':'11111','pageUnit':company_count}
url=requests.post("https://work.mma.go.kr/caisBYIS/search/byjjecgeomsaek.do",data=post_data)
bsObject=BeautifulSoup(url.text,"html.parser")
company_list=list()
for title in bsObject.find_all('th',{'class':'t-alignLt'}):
    temp_list=list()
    temp_list.append(title.text.replace("(주)","").replace("주식회사","").replace("(유)","").replace("㈜","").replace(" ",""))
    company_list.append(temp_list)
print(company_list)

for temp_list in company_list:
    info_list=list()
    try:
        bsObject=BeautifulSoup(requests.urlopen("http://www.saramin.co.kr/zf_user/search/company?searchword="+parse.quote(temp_list[0])))
        info_list.append("http://www.saramin.co.kr"+bsObject.find("a",{'class':'company_popup'}).get('href'))
    except:
        info_list.append("")
    try:
        bsObject=BeautifulSoup(requests.get("https://www.jobplanet.co.kr/search?query="+parse.quote(temp_list[0]),headers=headers).text)
        info_list.append("http://www.jobplanet.co.kr"+bsObject.find("a",{'class':'tit'}).get('href'))
    except Exception as e:
        print(e)
        info_list.append("")
    info_list.append("http://www.jobkorea.co.kr/Search/?stext="+parse.quote(temp_list[0]))
    temp_list.append(info_list)

for company in company_list:
    print(company)                                          