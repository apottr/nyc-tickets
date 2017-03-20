import requests,sys
from bs4 import BeautifulSoup
url = "http://nycserv.nyc.gov/NYCServWeb/NYCSERVMain"

headers = {
    'origin': "http://nycserv.nyc.gov",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'dnt': "1",
    'referer': "http://nycserv.nyc.gov/NYCServWeb/NYCSERVMain",
    'accept-encoding': "gzip, deflate",
    'accept-language': "en-US,en;q=0.8",
    'cache-control': "no-cache",
    'postman-token': "22275d28-1294-fa8c-2946-8b262ef2406e",
    }

def first_page(cookie):
    payload = {
        'AgencySelect': 'PVO',
        'AgencyType': 'at/PVO',
        'ChannelType': 'ct/Browser',
        'LinkType': 'EMPTY',
        'MethodName': 'NONE',
        'NycservRequest': "ChannelType=ct/Browser|RequestType=rt/Business|SubSystemType=st/Payments|AgencyType=at/PVO|ServiceName=PVO_FIND_TOWED_VEHICLE|MethodName=NONE|ParamCount=undefined|pvodropdownmenu=javascript:PVO_Find_Towed_Vehicle()|propertydropdownmenu=javascript:findPropertyTaxes('TAX_QUERY_SETUP','B')|waterdownmenu=javascript:waterChargeQuerySetup('DEP_WATER_CHARGE_QUERY_SETUP')|ecbdropdownmenu=javascript:environmentalBoardViolationsquerySetup('GET_ECB_VIOLATION_SEARCH_QUERY_SETUP')|requestahearingdropdownmenu=javascript:setServiceName('PVO_HEARING_QUERY_SETUP');submitProtocolForm();|AgencySelect=PVO|PageID=NYCSERVHome|SearchType=EMPTY|LinkType=EMPTY",
        'PageID': 'NYCSERVHome',
        'ParamCount': '0',
        'RequestType': 'rt/Business',
        'SearchType': 'EMPTY',
        'ServiceName': 'PVO_FIND_TOWED_VEHICLE',
        'SubSystemType': 'st/Payments',
        'ecbdropdownmenu': "javascript:environmentalBoardViolationsquerySetup('GET_ECB_VIOLATION_SEARCH_QUERY_SETUP')",
        'propertydropdownmenu': "javascript:findPropertyTaxes('TAX_QUERY_SETUP','B')",
        'pvodropdownmenu': "javascript:PVO_Find_Towed_Vehicle()",
        'requestahearingdropdownmenu': "javascript:setServiceName('PVO_HEARING_QUERY_SETUP');submitProtocolForm();",
        'waterdownmenu': "javascript:waterChargeQuerySetup('DEP_WATER_CHARGE_QUERY_SETUP')"
    }
    response = requests.request("POST", url, data=payload, headers=headers, cookies=cookie)
    return response

def second_page(cookie,plate,state,typ):
    payload = {
        'AgencyType': 'at/PVO',
        'ChannelType': 'ct/Browser',
        'MethodName': 'NONE',
        'NycservRequest': "ChannelType=ct/Browser|RequestType=rt/Business|SubSystemType=st/Payments|AgencyType=at/PVO|ServiceName=PVO_VIO_BY_PLATE_AND_TOW|MethodName=NONE|ParamCount=undefined|searchplate={num}|towcheck=true|selState={state}|selPlateType={type}|PageID=PVO_Find_Towed_Vehicle|PVO_VIOLATION_NUMBER=|PVO_PLATE_ID={num}|PVO_SEARCH_FOR_TOW=true|PVO_PLATE_TYPE={type}|PVO_STATE_NAME={state}".format(num=plate,state=state,type=typ),
        'PVO_PLATE_ID': plate,
        'PVO_PLATE_TYPE': typ,
        'PVO_SEARCH_FOR_TOW': 'true',
        'PVO_STATE_NAME': state,
        'PVO_VIOLATION_NUMBER': None,
        'PageID': 'PVO_Find_Towed_Vehicle',
        'ParamCount': '0',
        'RequestType': 'rt/Business',
        'ServiceName': 'PVO_VIO_BY_PLATE_AND_TOW',
        'SubSystemType': 'st/Payments',
        'searchplate': plate,
        'selPlateType': typ,
        'selState': state,
        'towcheck': 'true'
    }
    response = requests.request("POST", url, data=payload, headers=headers, cookies=cookie)
    return response

def strip_whitespace(lst):
    out = []
    for item in lst:
        out.append(item.strip())
    return out

def parse_html(html):
    soup = BeautifulSoup(html,'html.parser')
    one = soup.find_all('tr',class_='cellWhite')
    two = soup.find_all('tr',class_='cellLightBlue')
    out = []
    try:
        for item in one+two:
            for col in item.find_all('td',attrs={'width': '40'}):
                lst = col.find('a')['href'].split('\r\n')
                if len(lst) > 1:
                    out.append(strip_whitespace(lst)[4:len(lst)-1])
    except:
        pass

    return out
    

def main(plate):
    r = requests.get(url)
    r1 = first_page(r.cookies)
    r2 = second_page(r.cookies,plate,'NY','PAS')
    print parse_html(r2.text)


if __name__ == "__main__":
    main(sys.argv[1])
