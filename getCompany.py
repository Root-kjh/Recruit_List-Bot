import requests
from urllib import parse
from bs4 import BeautifulSoup
company_count=800
company_count=100
headers = {'User-Agent': 'Mozilla/5.0'}

def getCompanyInfo(companyName):
    info_list=dict()

    try:
        hostName="사람인"
        hostUri="http://www.saramin.co.kr"
        bsObject=BeautifulSoup(requests.get(hostUri+"/zf_user/search/company?searchword="+parse.quote(companyName),headers=headers).text)
        companyUri=hostUri+bsObject.find("div",{'class':'content'}).find("div",{'class':'item_corp'}).find("a").get('href')
        info_list.update({hostName:companyUri})
    except Exception as e:
        print(e)

    try:
        hostName="잡플레닛"
        hostUri="http://www.jobplanet.co.kr"
        bsObject=BeautifulSoup(requests.get(hostUri+"/search?query="+parse.quote(companyName),headers=headers).text)
        companyUri=hostUri+bsObject.find("a",{'class':'tit'}).get('href')
        info_list.update({hostName:companyUri})
    except Exception as e:
        print(e)

    try:
        hostName="잡코리아"
        hostUri="http://www.jobkorea.co.kr"
        bsObject=BeautifulSoup(requests.get(hostUri+"/Search/?stext="+parse.quote(companyName),headers=headers).text)
        companyUri=hostUri+bsObject.find("div",{'class':'corp-info'}).find("a").get('href')
        info_list.update({hostName:companyUri})
    except Exception as e:
        print(e)

    try:
        hostName="크레딧잡"
        hostUri="https://kreditjob.com"
        company_uri=hostUri+"/company/"+requests.get(hostUri+"/api/search/autocomplete?q="+parse.quote(companyName)+"&index=0&size=1").json()['docs'][0]['PK_NM_HASH']
        info_list.update({hostName:company_uri})
    except Exception as e:
        print(e)
    
    return info_list

def getRecruitList(companyName):
    Recruit_List=dict()

    # # 사람인
    # try:
    #     hostUri="http://www.saramin.co.kr"
    #     bsObject=BeautifulSoup(requests.get(hostUri+"/zf_user/search/company?searchword="+parse.quote(companyName),headers=headers).text)
    #     bsObject=BeautifulSoup(requests.get(hostUri+bsObject.find("div",{'class':'content'}).find("div",{'class':'item_corp'}).find("a",{'class':'cnt_ongoing'}).get('href')).text)
    #     for Recruit in bsObject.find("ul",{"class":"list_employ"}).findAll("a",{'class':'tit'}):
    #         Recruit_List.update({Recruit.text:hostUri+Recruit.get('href')})
    # except Exception as e:
    #     print(e)
    
    # # 잡플레닛
    # try:
    #     hostUri="https://www.jobplanet.co.kr"
    #     bsObject=BeautifulSoup(requests.get(hostUri+"/search?query="+parse.quote(companyName),headers=headers).text)
    #     bsObject=BeautifulSoup(requests.get(hostUri+bsObject.find("a",{'class':'tit'}).get('href').replace("info","job_postings")).text)
    #     for Recruit in bsObject.find("div",{"class":"job_items"}).findAll("div",{"class":"item_wrap"}):
    #         RecruitName=Recruit.find("h2",{"class":"tit"}).text
    #         RecruitUri=hostUri+Recruit.find("a",{"class":"job_item"}).get('href')
    #         Recruit_List.update({RecruitName:RecruitUri})
    # except Exception as e:
    #     print(e)

    # # 잡코리아
    # try:
    #     hostUri="http://www.jobkorea.co.kr"
    #     bsObject=BeautifulSoup(requests.get(hostUri+"/Search/?stext="+parse.quote(companyName),headers=headers).text)
    #     bsObject=BeautifulSoup(requests.get(hostUri+BeautifulSoup(requests.get(hostUri+bsObject.find("div",{'class':'corp-info'}).find("a").get('nav-src')).text).findAll("button",{"class":"btn-post-nav"})[1].get("src")).text)
    #     for Recruit in bsObject.findAll("a"):
    #         Recruit_List.update({Recruit.text:(hostUri+Recruit.get('href'))})
    # except Exception as e:
    #     print(e)

    # # 원티드
    # try:
    #     hostUri="https://www.wanted.co.kr"
    #     jsObject=requests.get(hostUri+"/api/v4/search?1583077171352&job_sort=job.latest_order&locations=seoul&years=0&country=kr&query="+parse.quote(companyName),headers=headers).json()
    #     for Recruit in jsObject['data']['jobs']:
    #         Recruit_List.update({Recruit['position']:hostUri+"/wd/"+str(Recruit['id'])})
    # except Exception as e:
    #     print(e)

    return Recruit_List


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
    print(temp_list[0])
    document=dict()
    document.update({"companyName":temp_list[0]})
    # company_list=getCompanyInfo(temp_list[0])
    Recruit_list=getRecruitList(temp_list[0])
    document.update(Recruit_list)
    print(document)