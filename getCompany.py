import requests
from urllib import parse
from bs4 import BeautifulSoup

company_count=800
company_count=5
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
    print(temp_list[0])

    #사람인
    try:
        bsObject=BeautifulSoup(requests.get("http://www.saramin.co.kr/zf_user/search/company?searchword="+parse.quote(temp_list[0]),headers=headers).text)
        info_list.append("http://www.saramin.co.kr"+bsObject.find("div",{'class':'content'}).find("div",{'class':'item_corp'}).find("a").get('href'))
    except Exception as e:
        print(e)
        info_list.append("")
    
    # #잡플레닛
    # try:
    #     bsObject=BeautifulSoup(requests.get("https://www.jobplanet.co.kr/search?query="+parse.quote(temp_list[0]),headers=headers).text)
    #     info_list.append("http://www.jobplanet.co.kr"+bsObject.find("a",{'class':'tit'}).get('href'))
    # except Exception as e:
    #     print(e)
    #     info_list.append("")

    # #잡코리아
    # try:
    #     bsObject=BeautifulSoup(requests.get("http://www.jobkorea.co.kr/Search/?stext="+parse.quote(temp_list[0]),headers=headers).text)
    #     info_list.append("http://www.jobkorea.co.kr"+bsObject.find("div",{'class':'corp-info'}).find("a").get('href'))
    # except Exception as e:
    #     print(e)
    #     info_list.append("")

    # #크레딧잡
    # try:
    #     company_uri="https://kreditjob.com/company/"+requests.get("https://kreditjob.com/api/search/autocomplete?q="+parse.quote(temp_list[0])+"&index=0&size=1").json()['docs'][0]['PK_NM_HASH']
    #     info_list.append(company_uri)
    # except Exception as e:
    #     print(e)
    #     info_list.append("")


    temp_list.append(info_list)

for temp_list in company_list:
    print(temp_list)