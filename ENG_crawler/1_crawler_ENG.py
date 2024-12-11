import time
import shutil
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import config

def setup_driver():
    """Setup Chrome driver with required options."""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("C:/下載程式/chromedriver-win64/chromedriver.exe")
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except SessionNotCreatedException as e:
        print("請確保您的 ChromeDriver 版本與 Chrome 瀏覽器匹配，您可以訪問 https://chromedriver.chromium.org/downloads 下載正確版本。")
        raise e
    return driver

def open_target_page(driver, target_url):
    """Open the target webpage and simulate clicking the bottom right corner."""
    driver.get(target_url)
    time.sleep(5)
    window_width = driver.execute_script("return window.innerWidth")
    window_height = driver.execute_script("return window.innerHeight")
    right_bottom_x = window_width - 10
    right_bottom_y = window_height - 10
    ActionChains(driver).move_by_offset(right_bottom_x, right_bottom_y).click().perform()
    print("點擊完成")

def scrape_data(driver, target_date):
    """Scrape articles data from the webpage."""
    data = []
    target_date_obj = datetime.strptime(target_date, "%Y%m%d")
    next_page_selector = "a[aria-label='Next Page']"

    while True:
        divs = driver.find_elements(By.CLASS_NAME, 'm-card.m-list-card')
        for div in divs:
            try:
                title = div.find_element(By.CLASS_NAME, 'm-card-title').find_element(By.TAG_NAME, 'b').text.strip()
            except NoSuchElementException:
                title = 'N/A'
            try:
                date = div.find_element(By.CLASS_NAME, 'm-card-info').text.strip()
                date_obj = datetime.strptime(date, "%m/%d/%Y")
                if date_obj < target_date_obj:
                    print("文章日期小於目標日期")
                    return data
            except (NoSuchElementException, ValueError):
                date = 'N/A'

            try:
                link = div.find_element(By.CLASS_NAME, 'm-card-title').find_element(By.TAG_NAME, 'a').get_attribute('href')
                full_link = "https://aws.amazon.com" + link if link.startswith('/') else link
            except NoSuchElementException:
                full_link = 'N/A'

            data.append({'Title': title, 'Date': date, 'URL': full_link})

        try:
            next_page = driver.find_element(By.CSS_SELECTOR, next_page_selector)
            next_page.click()
            time.sleep(5)
        except NoSuchElementException:
            print("找不到下一頁")
            break

    return data

def save_to_excel(data, save_path):
    """Save the scraped data to an Excel file."""
    df = pd.DataFrame(data)
    df['Content'] = ""
    try:
        df.to_excel(save_path, index=False)
        print("\n資料已成功儲存到", save_path)
        print (df.head())
    except PermissionError:
        print("無法儲存資料到", save_path, "，請確認檔案未被其他程序佔用並且有寫入權限。")
    except FileNotFoundError:
        print("無法找到儲存路徑", save_path, "，請確認路徑是否正確。")
    except Exception as e:
        print("儲存資料到 Excel 時發生未知錯誤：", str(e))

def main():
    target_date = config.target_date
    save_path = f"./articles/ENG_content_{target_date}.xlsx"
    target_url = "https://aws.amazon.com/new/?nc1=h_ls&whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&awsf.whats-new-categories=*all"

    driver = setup_driver()
    try:
        open_target_page(driver, target_url)
        data = scrape_data(driver, target_date)
        save_to_excel(data, save_path)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()