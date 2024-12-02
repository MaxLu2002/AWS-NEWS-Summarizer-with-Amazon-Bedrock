from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, NoSuchElementException
import pandas as pd
import openpyxl
import time
import shutil
import os
from datetime import datetime

save_path = "./content.xlsx"
target_date = "2024/11/21"
main_url = "https://aws.amazon.com/tw/new/?whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&awsf.whats-new-categories=*all"

# 設置 Chrome 瀏覽器選項
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 檢查 ChromeDriver 版本是否與 Chrome 匹配
chrome_version = shutil.which('chrome')
chromedriver_version = shutil.which('chromedriver')

# 初始化 WebDriver
service = Service("C:/下載程式/chromedriver-win64/chromedriver.exe")  # 確保 chromedriver 在 PATH 中
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
except SessionNotCreatedException as e:
    print("請確保您的 ChromeDriver 版本與 Chrome 瀏覽器匹配，您可以訪問 https://chromedriver.chromium.org/downloads 下載正確版本。")
    raise e

# 打開主頁面
driver.get(main_url)

# 等待 5 秒以確保頁面完全加載
time.sleep(5)

# 存儲結果的列表
data = []

# 定義下一頁的標籤
next_page_selector = "a[aria-label='下一頁']"

# 爬取當前頁面並循環至符合日期的所有頁面
while True:
    # 查找所有符合的<li>標籤，這些標籤包含文章資訊
    divs = driver.find_elements(By.CLASS_NAME, 'm-card.m-list-card')

    # 從每個<li>中提取標題、日期和鏈接
    for div in divs:
        try:
            title = div.find_element(By.CLASS_NAME, 'm-card-title').find_element(By.TAG_NAME, 'b').text.strip()
        except NoSuchElementException:
            title = 'N/A'
        
        try:
            date = div.find_element(By.CLASS_NAME, 'm-card-info').text.strip()
            date_obj = datetime.strptime(date, "%Y年%m月%d日")
            target_date_obj = datetime.strptime(target_date, "%Y/%m/%d")
            if date_obj < target_date_obj:
                # 如果文章日期小於目標日期，停止爬取
                driver.quit()
                # 使用 pandas 將資料轉換為 DataFrame
                df = pd.DataFrame(data)
                # 增加一個空欄位 "context"
                df['Context'] = ""
                print(df.head())
                # 將 DataFrame 儲存到 Excel，增加錯誤處理
                try:
                    df.to_excel(save_path, index=False)
                    print("資料已成功儲存到", save_path)
                except PermissionError:
                    print("無法儲存資料到", save_path, "。請確認檔案未被其他程序佔用並且有寫入權限。")
                except FileNotFoundError:
                    print("無法找到儲存路徑", save_path, "。請確認路徑是否正確。")
                except Exception as e:
                    print("儲存資料到 Excel 時發生未知錯誤：", str(e))
                exit()
        except (NoSuchElementException, ValueError):
            date = 'N/A'
        
        try:
            link = div.find_element(By.CLASS_NAME, 'm-card-title').find_element(By.TAG_NAME, 'a').get_attribute('href')
            full_link = "https://aws.amazon.com" + link if link.startswith('/') else link
        except NoSuchElementException:
            full_link = 'N/A'

        # 將資料添加到列表
        data.append({'Title': title, 'Date': date, 'URL': full_link})

    # 查找下一頁按鈕
    try:
        next_page = driver.find_element(By.CSS_SELECTOR, next_page_selector)
        next_page.click()
        # 等待頁面加載
        time.sleep(5)
    except NoSuchElementException:
        # 如果沒有找到下一頁按鈕，退出循環
        break

# 關閉 WebDriver
driver.quit()
