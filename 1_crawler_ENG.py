from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import shutil
from datetime import datetime
import var


target_date = var.ENG_target_date

save_path = f"./articles/ENG_content_{target_date}.xlsx"
target_url = "https://aws.amazon.com/new/?nc1=h_ls&whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&awsf.whats-new-categories=*all"


# -------------------------------------------------------- Chrome Setting --------------------------------------------------------
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
# -------------------------------------------------------- driver setting --------------------------------------------------------

headers = {
    ':authority': 'us-east-1.prod.pr.analytics.console.aws.a2z.com',
    ':method': 'POST',
    ':path': '/panoramaroute',
    ':scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US;q=0.9,zh-TW,zh;q=0.8,en;q=0.7',
    'content-length': '3417',
    'content-type': 'application/json; charset=UTF-8',
    'origin': 'https://aws.amazon.com',
    'panorama-appentity': 'aws-marketing',
    'priority': 'u=1, i',
    'referer': 'https://aws.amazon.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

# 使用 Chrome DevTools 協議來設置標頭
chrome_options.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})

# 啟動 driver 並套用標頭
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打開主頁面
driver.get(target_url)
time.sleep(5)
# 點擊螢幕右下角
window_width = driver.execute_script("return window.innerWidth")
window_height = driver.execute_script("return window.innerHeight")
right_bottom_x = window_width - 10
right_bottom_y = window_height - 10

# 模擬點擊右下角
ActionChains(driver).move_by_offset(right_bottom_x, right_bottom_y).click().perform()
print("點擊完成")

# -------------------------------------------------------- crawler --------------------------------------------------------
# 爬取當前頁面並循環至符合日期的所有頁面
data = []
while True:
    # 查找所有符合的<li>標籤，這些標籤包含文章資訊
    divs = driver.find_elements(By.CLASS_NAME, 'm-card.m-list-card')
    next_page_selector = "a[aria-label='Next Page']"
    # 從每個<li>中提取標題、日期和鏈接
    for div in divs:
        try:
            title = div.find_element(By.CLASS_NAME, 'm-card-title').find_element(By.TAG_NAME, 'b').text.strip()
        except NoSuchElementException:
            title = 'N/A'
        try:
            date = div.find_element(By.CLASS_NAME, 'm-card-info').text.strip()
            date_obj = datetime.strptime(date, "%m/%d/%Y")
            target_date_obj = datetime.strptime(target_date, "%Y%m%d")
            if date_obj < target_date_obj:
                # 如果文章日期小於目標日期，停止爬取
                driver.quit()
                print("文章日期小於目標日期")
                # 使用 pandas 將資料轉換為 DataFrame
                df = pd.DataFrame(data)
                # 增加一個空欄位 "context"
                df['Content'] = ""
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
        print ("找不到下一頁")
    # 關閉 WebDriver
    driver.quit()

    # 使用 pandas 將資料轉換為 DataFrame
    df = pd.DataFrame(data)
    # 增加一個空欄位 "content"
    df['Content'] = ""
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

