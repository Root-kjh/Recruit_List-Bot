import requests
from urllib import parse
from bs4 import BeautifulSoup
import warnings
from datetime import datetime
import pymongo


conn=pymongo.MongoClient('recruit-list.kro.kr')
collection=conn.get_database('Recruit_List').get_collection('company')
collection.remove({})
warnings.simplefilter("ignore", UserWarning)
company_count=800
headers = {'User-Agent': 'Mozilla/5.0'}
companyInfoSites=["사람인","잡플레닛","잡코리아","크레딧잡"]
companyInfoUris=["http://www.saramin.co.kr","http://www.jobplanet.co.kr","http://www.jobkorea.co.kr","https://kreditjob.com"]

def getCompanyInfoDict(siteName,uri):
    return {"siteName":siteName,"uri":uri}

def getCompanyInfoSite(companyName):
    info_list=list()
    try:
        hostName=companyInfoSites[0]
        hostUri=companyInfoUris[0]
        bsObject=BeautifulSoup(requests.get(hostUri+"/zf_user/search/company?searchword="+parse.quote(companyName),headers=headers).text)
        companyUri=hostUri+bsObject.find("div",{'class':'content'}).find("div",{'class':'item_corp'}).find("a").get('href')
        info_list.append(getCompanyInfoDict(hostName,companyUri))
    except Exception as e:
        pass

    try:
        hostName=companyInfoSites[1]
        hostUri=companyInfoUris[1]
        bsObject=BeautifulSoup(requests.get(hostUri+"/search?query="+parse.quote(companyName),headers=headers).text)
        companyUri=hostUri+bsObject.find("a",{'class':'tit'}).get('href')
        info_list.append(getCompanyInfoDict(hostName,companyUri))
    except Exception as e:
        pass

    try:
        hostName=companyInfoSites[2]
        hostUri=companyInfoUris[2]
        bsObject=BeautifulSoup(requests.get(hostUri+"/Search/?stext="+parse.quote(companyName),headers=headers).text)
        companyUri=hostUri+bsObject.find("div",{'class':'corp-info'}).find("a").get('href')
        info_list.append(getCompanyInfoDict(hostName,companyUri))
    except Exception as e:
        pass

    try:
        hostName=companyInfoSites[3]
        hostUri=companyInfoUris[3]
        companyUri=hostUri+"/company/"+requests.get(hostUri+"/api/search/autocomplete?q="+parse.quote(companyName)+"&index=0&size=1").json()['docs'][0]['PK_NM_HASH']
        info_list.append(getCompanyInfoDict(hostName,companyUri))
    except Exception as e:
        pass
    
    return info_list

def getRecruitDict(siteName,uri):
    return {"siteName":siteName,"uri":uri}

def getRecruitList(companyName):
    Recruit_List=list()

    # 사람인
    try:
        hostUri="http://www.saramin.co.kr"
        bsObject=BeautifulSoup(requests.get(hostUri+"/zf_user/search/company?searchword="+parse.quote(companyName),headers=headers).text)
        bsObject=BeautifulSoup(requests.get(hostUri+bsObject.find("div",{'class':'content'}).find("div",{'class':'item_corp'}).find("a",{'class':'cnt_ongoing'}).get('href')).text)
        for Recruit in bsObject.find("ul",{"class":"list_employ"}).findAll("a",{'class':'tit'}):
            Recruit_List.append(getRecruitDict(Recruit.text,hostUri+Recruit.get('href')))
    except Exception as e:
        pass
    
    # 잡플레닛
    try:
        hostUri="https://www.jobplanet.co.kr"
        bsObject=BeautifulSoup(requests.get(hostUri+"/search?query="+parse.quote(companyName),headers=headers).text)
        bsObject=BeautifulSoup(requests.get(hostUri+bsObject.find("a",{'class':'tit'}).get('href').replace("info","job_postings")).text)
        for Recruit in bsObject.find("div",{"class":"job_items"}).findAll("div",{"class":"item_wrap"}):
            RecruitName=Recruit.find("h2",{"class":"tit"}).text
            RecruitUri=hostUri+Recruit.find("a",{"class":"job_item"}).get('href')
            Recruit_List.append(getRecruitDict(RecruitName,RecruitUri))
    except Exception as e:
        pass

    # 잡코리아
    try:
        hostUri="http://www.jobkorea.co.kr"
        bsObject=BeautifulSoup(requests.get(hostUri+"/Search/?stext="+parse.quote(companyName),headers=headers).text)
        bsObject=BeautifulSoup(requests.get(hostUri+BeautifulSoup(requests.get(hostUri+bsObject.find("div",{'class':'corp-info'}).find("a").get('nav-src')).text).findAll("button",{"class":"btn-post-nav"})[1].get("src")).text)
        for Recruit in bsObject.findAll("a"):
            Recruit_List.append(getRecruitDict(Recruit.text,hostUri+Recruit.get('href')))
    except Exception as e:
        pass

    # 원티드
    try:
        hostUri="https://www.wanted.co.kr"
        jsObject=requests.get(hostUri+"/api/v4/search?1583077171352&job_sort=job.latest_order&locations=seoul&years=0&country=kr&query="+parse.quote(companyName),headers=headers).json()
        for Recruit in jsObject['data']['jobs']:
            Recruit_List.append(getRecruitDict(Recruit['position'],hostUri+"/wd/"+str(Recruit['id'])))
    except Exception as e:
        pass

    return Recruit_List

def crawlingCompanyInfo(siteIdx,siteUri):
    companyInfo=dict()
    if siteIdx==2:
        try:
            bsObject=BeautifulSoup(requests.get(siteUri,headers=headers).text)
            employeesNum=int((bsObject.findAll("div",{"class":"value"})[3].text).replace("명",""))
            foundingYear=int((bsObject.findAll("div",{"class":"value"})[5].text).split(".")[0])
            companyInfo['employeesNum']=employeesNum
            companyInfo['foundingYear']=foundingYear
            return companyInfo
        except:
            pass
    elif siteIdx==3:
        try:
            jsObject=requests.post("https://kreditjob.com/api/company/companyPage",data={'PK_NM_HASH':siteUri.split("/")[-1]},headers=headers).json()
            employeesNum=int(jsObject['companyInfoData']['PRSN_BASE'])
            foundingYear=datetime.today().year-int(jsObject['companyInfoData']['COMPANY_AGE'])
            companyInfo['employeesNum']=employeesNum
            companyInfo['foundingYear']=foundingYear
            return companyInfo
        except:
            pass
    return -1

def getCompanyInfo(siteDoc):
    try:
        siteName=siteDoc['siteName']
    except:
        return -1
    for i in range(len(companyInfoSites)):
        if siteName==companyInfoSites[i] and (i==2 or i==3):
            return crawlingCompanyInfo(i,siteDoc['uri'])
    return -1

post_data={'al_eopjong_gbcd':'11111','eopjong_gbcd_list':'11111','eopjong_gbcd':'1','eopjong_cd':'11111','pageUnit':company_count}
url=requests.post("https://work.mma.go.kr/caisBYIS/search/byjjecgeomsaek.do",data=post_data)
bsObject=BeautifulSoup(url.text,"html.parser")
company_list=list()
for title in bsObject.find_all('th',{'class':'t-alignLt'}):
    temp_list=list()
    temp_list.append(title.text.replace("(주)","").replace("주식회사","").replace("(유)","").replace("㈜","").replace(" ",""))
    company_list.append(temp_list)

for temp_list in company_list:
    print(temp_list[0])
    document=dict()
    document['companyName']=temp_list[0]
    company_list=getCompanyInfoSite(temp_list[0])
    Recruit_list=getRecruitList(temp_list[0])
    for companySite in company_list:
        result=getCompanyInfo(companySite)
        if result!=-1:
            document['foundingYear']=result['foundingYear']
            document['employeesNum']=result['employeesNum']
            break
    document['companyInfos']=company_list
    document['recruitmentNotices']=Recruit_list
    collection.insert(document)