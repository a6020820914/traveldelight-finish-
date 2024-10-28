# -*- coding: utf-8 -*-
"""
雄獅旅遊

**如果有增減爬蟲的欄位需修改
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import threading
import queue
import time

ArriveID={
    # "台灣":"--9,",
    # "北基宜":"-51-9,",
    # "桃竹苗":"-52-9,",
    # "中彰投":"-53-9,",
    # "雲嘉南":"-54-9,",
    # "高屏":"-55-9,",
    # "花東":"-56-9,",
    # "離島":"-57-9,",
    "台北":"AA-51-9,",
    "基隆":"AB-51-9,",
    "宜蘭":"AC-51-9,",
    "新北":"Z9-51-9,",
    "桃園":"AD-52-9,",
    "新竹":"AE-52-9,",
    "苗栗":"AF-52-9,",
    "台中":"AG-53-9,",
    "彰化":"AH-53-9,",
    "南投":"AI-53-9,",
    "雲林":"AJ-54-9,",
    "嘉義":"AK-54-9,",
    "台南":"AL-54-9,",
    "高雄":"AM-55-9,",
    "屏東":"AN-55-9,",
    "小琉球":"B3-55-9,",
    "花蓮":"AO-56-9,",
    "台東":"AP-56-9,",
    "蘭嶼":"AQ-56-9,",
    "綠島":"AR-56-9,",
    "澎湖":"AS-57-9,",
    "金門":"AT-57-9,",
    "馬祖":"AU-57-9," 
 }

Arrivelist=list(ArriveID.keys())
# print(Arrivelist)
# print("="*20)
# Arrive=input('地點:')
# GoDateStart=input('去日(ex.2024-12-23):')
# GoDateEnd=input('返日(ex.2024-12-23):')
# Arrivelist=["台北"]
"""
設定年月日
"""
GoDateStart=datetime.now().strftime("%Y-%m-%d")
GoDateEnd=datetime.today().date()-relativedelta(months=-3)
GoDateEnd=GoDateEnd.strftime("%Y-%m-%d")

#更新data用的暫存欄位
indexes=[]
earlierGoDatevalues=[]
renew_datevalues=[]
GoDatevalues=[]
AttractionSet=set()

"""
擷取
"""
def liontravel(Arrive, df):
    """
    設定欄位
    """
    #新增data用的暫存欄位
    NormGroupIDList=[]
    TourNamelist=[]
    TourSitelist=[]
    CompanyList=[]
    TourLinklist=[]
    GoSitelist=[]
    TourImagelist=[]
    TourDaylist=[]
    Pricelist=[]
    EarliGoDatelist=[]
    CreateDateList=[]
    RenewDateList=[]
    TourSpecialeList=[]
    GoDatelist=[]
    Attractionlist=[]
    Breakfastlist=[]
    Dinnerlist=[]
    Lunchlist=[]
    Daylist=[]
    TravelPointlist=[]
    Hotellist=[]
    
    """
    取得頁數
    """
    myheader={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
    link='https://travel.liontravel.com/search?DepartureID=&ArriveID='+ArriveID[Arrive]+'&GoDateStart='+GoDateStart+'&GoDateEnd='+GoDateEnd+'&Keywords=&TravelType=1&IsSold=true&Platform=APP'
    
    payload = {"ArriveID":ArriveID[Arrive],
                "GoDatestart":GoDateStart,
                "GroupID":None,
                "Keywords":"",
                "IsEnsureGroup":None,
                "IsSold":True,
                "ThemeID":None,
                "TravelPavilionGroupID":None,
                "KeywordsCity":None,
                "TravelType":1,
                "BuIDs":"",
                "PreferAirlines":None,
                "GoDateEnd":GoDateEnd,
                "DepartureID":"",
                "WeekDay":"",
                "PriceList":None,
                "AirlineIDs":"",
                "TripTypes":"",
                "Tags":"",
                "SortType":3,
                "Days":"",
                "Page":1,
                "PageSize":10}
    response = requests.post(
        'https://travel.liontravel.com/search/grouplistinfojson'
        , data=payload)
    TotalPages = response.json()['TotalPage']  # 存取TotalPage欄位

    """
    開始擷取
    """
    x=True
    while x:
        #翻頁
        for i in range(1, TotalPages+1):
            payload = {"ArriveID":ArriveID[Arrive],
                        "GoDatestart":GoDateStart,
                        "GroupID":None,
                        "Keywords":"",
                        "IsEnsureGroup":None,
                        "IsSold":True,
                        "ThemeID":None,
                        "TravelPavilionGroupID":None,
                        "KeywordsCity":None,
                        "TravelType":1,
                        "BuIDs":"",
                        "PreferAirlines":None,
                        "GoDateEnd":GoDateEnd,
                        "DepartureID":"",
                        "WeekDay":"",
                        "PriceList":None,
                        "AirlineIDs":"",
                        "TripTypes":"",
                        "Tags":"",
                        "SortType":3,
                        "Days":"",
                        "Page":i,
                        "PageSize":10}
            response = requests.post(
                'https://travel.liontravel.com/search/grouplistinfojson'
                , data=payload)
            r=requests.get(link, headers=myheader)
            if r.status_code==requests.codes.ok:
                normGroupLists = response.json()['NormGroupList']  # 存取NormGroupList欄位
            #取得該頁的旅遊資訊
            for _, normGroupList in enumerate(normGroupLists):
                NormGroupID = normGroupList['NormGroupID']
                GroupIDs = normGroupList['GroupList'][0]['GroupID']
                # 如果已經有的行程
                if NormGroupID in list(df["NormGroupID"]):
                    indexes.append(list(df["NormGroupID"]).index(NormGroupID))
                    earlierGoDatevalues.append(normGroupList['GroupList'][0]['GoDate'])
                    renew_datevalues.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    r1=requests.get('https://travel.liontravel.com/detail?NormGroupID='+NormGroupID+'&GroupID='+GroupIDs+'&Platform=app', headers=myheader)
                    time.sleep(1)
                    if r1.status_code==requests.codes.ok:
                        GoDate=[]
                        payload2 = {"NormGroupID":NormGroupID,"GoDateStart":GoDateStart,"GoDateEnd":GoDateEnd,"TourID":"","preferairlines":""}
                        response2 = requests.post(
                            'https://travel.liontravel.com/detail/groupcalendarjson'
                            , data=payload2)
                        dates=response2.json()
                        for d in dates:
                            GoDate.append(d['Date'])
                        GoDatevalues.append(GoDate)
                # 如果還沒有的行程
                else:
                    GroupIDs = normGroupList['GroupList'][0]['GroupID']
                    NormGroupIDList.append(NormGroupID)
                    TourNamelist.append(normGroupList['TourName'])
                    TourSitelist.append(Arrive)
                    CompanyList.append('雄獅旅遊')
                    TourLinklist.append('https://travel.liontravel.com/detail?NormGroupID='+NormGroupID+'&GroupID='+GroupIDs+'&Platform=app')
                    TourImagelist.append(normGroupList['ImgM'])   
                    TourDaylist.append(normGroupList['TourDays'])  
                    GoSitelist.append(['新北' if i['CityName'] == '新北市' else i['CityName'] for i in normGroupList['StartFromCityList']])
                    Pricelist.append(normGroupList['GroupStraightPrice'].replace(',',''))
                    EarliGoDatelist.append(normGroupList['GroupList'][0]['GoDate'])
                    CreateDateList.append(datetime.now().strftime("%Y-%m-%d"))
                    RenewDateList.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    r1=requests.get('https://travel.liontravel.com/detail?NormGroupID='+NormGroupID+'&GroupID='+GroupIDs+'&Platform=app', headers=myheader)
                    time.sleep(1)
                    if r1.status_code==requests.codes.ok:
                        soup = BeautifulSoup(r1.text, 'html.parser')
                        TourID = soup.select('div#clickPara')[0]['data-tourid']
                        payload1 = {"TourID":TourID,"IsPreview":False,"TravelType":1}
                        response1 = requests.post(
                            'https://travel.liontravel.com/detail/daytripinfojson'
                            , data=payload1)      
                        TDHDesc = response1.json()['TDHDesc']  # 存取TDHDesc欄位
                        TourSpecialeList.append(TDHDesc)
                        DailyLists = response1.json()['DailyList']  # 存取DailyList欄位
                        
                        Breakfast=[Daily['Breakfast'] for Daily in DailyLists]
                        Dinner=[Daily['Dinner'] for Daily in DailyLists]
                        Lunch=[Daily['Lunch'] for Daily in DailyLists]
                        Day=[Daily['Day'] for Daily in DailyLists]

                        TravelPoint=[]
                        Hotel=[]
                        Attraction=[]
                        for Daily in DailyLists:
                            a=[d['Name'] for d in Daily['AttractionsList']]
                            for i in a:
                                Attraction.append(i)
                            d = Daily['TravelPoint']
                            d = d.replace('<span class="icon ic-ln iairplane"></span>', "→")
                            d = d.replace('<span class="icon ic-ln ibus"></span>', "→")
                            d = d.replace('<span class="icon ic-ln iboat"></span>', "→")
                            d = d.replace('<span class="icon ic-ln iwalk"></span>', "→")
                            d = d.replace('<span class="icon ic-ln itrain"></span>', "→")
                            d = d.replace('<span class="icon ic-ln ibike"></span>', "→")
                            d = d.replace("<font face='微軟正黑體' size='3'>", "")
                            TravelPoint.append(d)
                            h = ' 或 '.join([i['Name'] for i in Daily['HotelList']])
                            Hotel.append(h)


                        for a in Attraction:
                            AttractionSet.add(a)
                        Attractionlist.append(Attraction)
                        Breakfastlist.append(Breakfast)
                        Dinnerlist.append(Dinner)
                        Lunchlist.append(Lunch)
                        Daylist.append(Day)
                        TravelPointlist.append(TravelPoint)
                        Hotellist.append(Hotel)
                        GoDate=[]
                        payload2 = {"NormGroupID":NormGroupID,"GoDateStart":GoDateStart,"GoDateEnd":GoDateEnd,"TourID":"","preferairlines":""}
                        response2 = requests.post(
                            'https://travel.liontravel.com/detail/groupcalendarjson'
                            , data=payload2)
                        dates=response2.json()
                        for d in dates:
                            GoDate.append(d['Date'])
                        GoDatelist.append(GoDate)
                        break
                break
            break
        x=False
    """
    儲存擷取結果
    """
    data = pd.DataFrame({"NormGroupID":NormGroupIDList,"tourname":TourNamelist,"toursite":TourSitelist,"company":CompanyList,
                         "tourlink":TourLinklist,"gosite":GoSitelist,"tourimage":TourImagelist,"tourday":TourDaylist,"price":Pricelist,
                         "earlierGoDate":EarliGoDatelist,"create_date":CreateDateList,"renew_date":RenewDateList,"tourSpecial":TourSpecialeList,
                         'GoDate':GoDatelist, 'Attraction':Attractionlist, 'Day':Daylist, 'TravelPoint':TravelPointlist, 
                         'Breakfast':Breakfastlist, 'Lunch':Lunchlist, 'Dinner':Dinnerlist, 'Hotel':Hotellist})
    return data

"""
多工+貯列
"""    
class Worker(threading.Thread):
    def __init__(self, queue, lock, df):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.df = df

    def run(self):
        while self.queue.qsize() > 0:
          # 取得新的資料
          Arrive=self.queue.get()

          
          result_data = liontravel(Arrive, self.df)
          if not result_data.empty:
                self.lock.acquire()  # 鎖住寫檔操作
                try:
                    df=pd.read_csv('liontravel.csv', encoding='ansi', index_col=0)
                    con = pd.concat([df,result_data],ignore_index=True)
                    con.to_csv('liontravel.csv', encoding='ansi',errors='ignore')
                finally:
                    self.lock.release()  # 釋放鎖
               
"""
擷取各旅遊地點資訊+存檔
"""
lock = threading.Lock()
my_queue = queue.Queue()
    
# 將任務放入佇列（每個地點的工作）
for Arrive in Arrivelist:
    my_queue.put(Arrive)

# 建立10個工作者執行緒
num_threads = 4
workers = []

"""
取得資料(多工+鎖)
"""
df=pd.read_csv('liontravel.csv', encoding='ansi', index_col=0)
for _ in range(num_threads):
    worker = Worker(my_queue, lock, df)
    worker.start()
    workers.append(worker)

# 等待所有工作者完成
for worker in workers:
    worker.join()

df1=pd.read_csv('liontravel.csv', encoding='ansi', index_col=0)
for idx, ev, rv, gv in zip(indexes, earlierGoDatevalues, renew_datevalues, GoDatevalues):
    df1.at[idx, "earlierGoDate"]=ev
    df1.at[idx, "renew_date"]=rv
    df1.at[idx, "GoDate"]=gv
df1.to_csv('liontravel.csv', encoding='ansi',errors='ignore')  

if len(AttractionSet)>0:
    for r in ['', '高雄文化中心五福路正門口前集合上車', '台南美術2館(忠義小學大門對面)上車', 
              '台鐵新左營站1樓', '預計抵達出發地', '高鐵嘉義站', '返程', '飯店集合出發', '金門尚義機場',
              '準備返程', '飯店CHECK-OUT', '民宿早餐', '台北火車站／北二門內／站前門市','\\u200b漂浮西洋棋盤',
              'Good Morning！讓柔和的太陽光喚醒您的早晨～請自行前往餐廳享用飯店美味豐富的早餐唷！']:
        try:
            AttractionSet.remove(r)
        except:
            continue
    df2=pd.read_csv('attraction.csv', encoding='ansi', index_col=0)
    df2_Attract=set(df2['Attraction'])
    Attract=df2_Attract|AttractionSet
    Attractdata = pd.DataFrame({"Attraction":list(Attract)})
    Attractdata.to_csv('attraction.csv', encoding='ansi',errors='ignore')      
 
  