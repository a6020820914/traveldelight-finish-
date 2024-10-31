from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def initialize_driver():
    options = Options()
    options.add_argument('--headless')  # 如果不需要無頭模式，則移除這一行
    options.add_argument('--no-sandbox')  # Heroku 上可能需要這些選項
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver