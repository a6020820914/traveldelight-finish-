# -*- coding: utf-8 -*-
"""
五福旅行社
"""
import os
import threading
import queue
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless=old") #無頭模式
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

#佈署所需要的設定
from selenium.webdriver.chrome.service import Service
service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
# myheader={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3'}


"""
設定旅遊地點
"""
ArriveID={
    # "台灣":"allarea",
    "台北":"sarea00178",
    "基隆":"sarea00421",
    "宜蘭":"sarea00179",
    # "新北":"sarea00178",
    "桃園":"sarea00478",
    "新竹":"sarea00479",
    "苗栗":"sarea00480",
    "台中":"sarea00183",
    "彰化":"sarea00184",
    "南投":"sarea00185",
    "雲林":"sarea00186",
    "嘉義":"sarea00187",
    "台南":"sarea00188",
    "高雄":"sarea00484",
    "屏東":"sarea00485",
    "小琉球":"sarea00481",
    "花蓮":"sarea00194",
    "台東":"sarea00195",
    "蘭嶼":"sarea00197",
    "綠島":"sarea00196",
    "澎湖":"sarea00193",
    "金門":"sarea00191",
    "馬祖":"sarea00192" 
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
GoDateStart=GoDateStart.replace("-", "/")
GoDateEnd=GoDateEnd.replace("-", "/")

#更新data用的暫存欄位
indexes=[]
earlierGoDatevalues=[]
GoDatevalues=[]
renew_datevalues=[]



"""
擷取
"""
def domestic(Arrive, df, driver):
    
    """
    設定欄位
    """
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
    TourSpecialList=[]
    GoDatelist=[]
    Attractionlist=[]
    Breakfastlist=[]
    Dinnerlist=[]
    Lunchlist=[]
    Daylist=[]
    TravelPointlist=[]
    Hotellist=[]
    
    # link='https://domestic.lifetour.com.tw/searchlist/111/allarea?datefrom='+GoDateStart+'&dateto='+GoDateEnd+'&order=1&standby=1'
    link='https://domestic.lifetour.com.tw/searchlist/111/'+ArriveID[Arrive]+'?datefrom='+GoDateStart+'&dateto='+GoDateEnd+'&order=1&standby=1'
    # link='https://domestic.lifetour.com.tw/'

    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1920,1080)
    driver.implicitly_wait(15)
    driver.get(link)
    time.sleep(1)
    objects=driver.find_elements(By.CSS_SELECTOR, 'div.item.item-list.rel-content')
    num1=len(objects)
    num0=0
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(1)
    while num1!=num0:
        objects=driver.find_elements(By.CSS_SELECTOR, 'div.item.item-list.rel-content')
        num0=len(objects)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)
        objects=driver.find_elements(By.CSS_SELECTOR, 'div.item.item-list.rel-content')
        num1=len(objects)
        time.sleep(1)
    
    links = [l.get_attribute('href') for l in driver.find_elements(By.CSS_SELECTOR, 'div.item-body div.item-title a')]
    TourNames=[i.text for i in driver.find_elements(By.CSS_SELECTOR, 'div.item.item-list.rel-content div.item-title a')]
    TourSites=[i.text.split(', ')[0].split('/')[0].rstrip('市').rstrip('縣') for i in driver.find_elements(By.CSS_SELECTOR, 'div.item.item-list.rel-content div.item-localtion')]
    TourImages=[i.get_attribute('style').split('(')[1].split(')')[0].replace('"', '') for i in driver.find_elements(By.CSS_SELECTOR, 'div.item-img a')]
    Prices=[i.text.split('\n')[0].rstrip('起元').replace(',', '') for i in driver.find_elements(By.CSS_SELECTOR, 'div.item.item-list.rel-content div.item-cost div.item-price div.price')]

    for lin, tn, ts, tm, p in zip(links, TourNames, TourSites, TourImages, Prices):
        
        NormGroupID=lin.lstrip('https://domestic.lifetour.com.tw/detail/').split('#')[0]
        if NormGroupID in list(df["NormGroupID"]):
            indexes.append(list(df["NormGroupID"]).index(NormGroupID))            
            renew_datevalues.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            driver.get(lin)
            time.sleep(2)
            WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.text.fs-18.c-green')))
            earlierGoDatevalues.append('2024/'+driver.find_element(By.CSS_SELECTOR, 'div.text.fs-18.c-green').text.replace('月', '/').replace('日', ''))
            GoDates=[]
            go=True
            n=0
            while go:                
                try:
                    WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div.mb-content ul li[data-mcode="{NormGroupID}"]')))
                    Dates=[d.get_attribute('data-date') for d in driver.find_elements(By.CSS_SELECTOR, f'div.mb-content ul li[data-mcode="{NormGroupID}"]')]
                except:
                    go=False
                for date in Dates:
                    GoDates.append(date)
                if n == 2:
                    go=False
                else:
                    driver.find_element(By.CSS_SELECTOR, 'div#calendar div.head a.next').click()   
                    n+=1
                time.sleep(1)                    
            GoDatevalues.append(GoDates)
            
        else:
            NormGroupIDList.append(NormGroupID)
            TourNamelist.append(tn)
            TourSitelist.append(ts)
            TourLinklist.append(lin)
            TourImagelist.append(tm)
            Pricelist.append(p)
            driver.get(lin)
            time.sleep(2)
            WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.dis-flex.ai-bl.wt100 div.text.fs-18')))
            GoSitelist.append([driver.find_element(By.CSS_SELECTOR, 'div.dis-flex.ai-bl.wt100 div.text.fs-18').text[:2]])
            TourDay=driver.find_elements(By.CSS_SELECTOR, 'div.dis-flex.ai-bl.wt50 div.text.fs-18')[1].text.split('天')[0]
            TourDaylist.append(TourDay)
            EarliGoDatelist.append('2024/'+driver.find_element(By.CSS_SELECTOR, 'div.text.fs-18.c-green').text.replace('月', '/').replace('日', ''))
            CompanyList.append('五福旅遊')
            CreateDateList.append(datetime.now().strftime("%Y-%m-%d")) 
            RenewDateList.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            TourSpecialList.append('')
            Attractionlist.append([])
            
            GoDates=[]
            go=True
            n=0
            while go:
                try:
                    WebDriverWait(driver,20,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div.mb-content ul li[data-mcode="{NormGroupID}"]')))
                    Dates=[d.get_attribute('data-date') for d in driver.find_elements(By.CSS_SELECTOR, f'div.mb-content ul li[data-mcode="{NormGroupID}"]')]
                except:
                    go=False
                for date in Dates:
                    GoDates.append(date)
                if n == 2:
                    go=False
                else:
                    driver.find_element(By.CSS_SELECTOR, 'div#calendar div.head a.next').click()   
                    n+=1
                time.sleep(1)
            GoDatelist.append(GoDates)
                        
            Daylist.append([day for day in range(1, int(TourDay)+1)])            
            TravelPointlist.append([])
            
            Breakfasts=[]
            Lunchs=[]
            Dinners=[]
            meals=driver.find_elements(By.CSS_SELECTOR, 'div.wrap-box div.wrap-meal div.text')# div.text div
            for m in meals:
                try:
                    Breakfast=m.text.lstrip('早餐').split('午餐')[0].strip('\n')
                except:
                    Breakfast=''
                Breakfasts.append(Breakfast)
                try:
                    Lunch=m.text.split('午餐')[1].split('晚餐')[0].strip('\n')
                except:
                    Lunch=''
                Lunchs.append(Lunch)
                try:
                    Dinner=m.text.split('晚餐')[1].strip('\n')
                except:
                    Dinner=''
                Dinners.append(Dinner)
            Breakfastlist.append(Breakfasts)
            Lunchlist.append(Lunchs)
            Dinnerlist.append(Dinners)             
            try:
                Hotels=[h.text for h in driver.find_elements(By.CSS_SELECTOR, 'div.wrap-box div.wrap-hotel div.text')]
            except:
                Hotels=['']
            Hotellist.append(Hotels) 
    
    """
    回傳新擷取結果
    """    
    data = pd.DataFrame({"NormGroupID":NormGroupIDList,"tourname":TourNamelist,"toursite":TourSitelist,"company":CompanyList,
                          "tourlink":TourLinklist,"gosite":GoSitelist,"tourimage":TourImagelist,"tourday":TourDaylist,"price":Pricelist,
                          "earlierGoDate":EarliGoDatelist,"create_date":CreateDateList,"renew_date":RenewDateList,"tourSpecial":TourSpecialList,
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
        # 初始化 WebDriver
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def run(self):
        while self.queue.qsize() > 0:
          # 取得新的資料
            Arrive=self.queue.get()
            
            result_data = domestic(Arrive, self.df, self.driver)
            """
            取得資料(鎖)
            """
            if not result_data.empty:
                self.lock.acquire()  # 鎖住寫檔操作
                try:
                    df=pd.read_csv('domestic.csv', encoding='ansi', index_col=0)
                    con = pd.concat([df,result_data],ignore_index=True)
                    con.to_csv('domestic.csv', encoding='ansi',errors='ignore')
                finally:
                    self.lock.release()  # 釋放鎖
                    
    # 在程式結束時，確保 WebDriver 被正確關閉                
    def quit_driver(self):
        self.driver.quit()


               
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

df=pd.read_csv('domestic.csv', encoding='ansi', index_col=0)
for _ in range(num_threads):
    worker = Worker(my_queue, lock, df)
    worker.start()
    workers.append(worker)
   
    
# 等待所有工作者完成
for worker in workers:
    worker.join()
    
for worker in workers:
    worker.quit_driver()

df1=pd.read_csv('domestic.csv', encoding='ansi', index_col=0)
for idx, ev, rv, gv in zip(indexes, earlierGoDatevalues, renew_datevalues, GoDatevalues):
    df1.at[idx, "earlierGoDate"]=ev
    df1.at[idx, "renew_date"]=rv
    df1.at[idx, "GoDate"]=gv
df1.to_csv('domestic.csv', encoding='ansi',errors='ignore')

# if len(AttractionSet)>0:       
#     df2=pd.read_csv('attraction.csv', encoding='ansi', index_col=0)
#     df2_Attract=set(df2['Attraction'])
#     Attract=df2_Attract|AttractionSet
#     Attractdata = pd.DataFrame({"Attraction":list(Attract)})
#     Attractdata.to_csv('attraction.csv', encoding='ansi',errors='ignore')
