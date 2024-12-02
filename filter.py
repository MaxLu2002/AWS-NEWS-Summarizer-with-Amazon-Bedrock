import pandas as pd
import requests
from bs4 import BeautifulSoup
import var

# 設定目標檔案
target_date = var.target_date
target_file = f'./content_{target_date}.xlsx'

# 讀取 Excel 檔案
df = pd.read_excel(target_file)
links = df['URL']
links = df['URL'].apply(lambda x: x.replace('aws.amazon.com/about-aws', 'aws.amazon.com/tw/about-aws'))

# 初始化空的內容列表
contents = []

# 依次訪問每個連結並爬取內文
for link in links:
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # 爬取指定標籤的內文
        content_tags = soup.find_all('div', class_='wn-body')
        content = content_tags[1].get_text(strip=True) if len(content_tags) > 1 else ''
    except requests.RequestException as e:
        content = f'Error: {e}'
    contents.append(content)
    print (f"{link}爬取完成")

# 將爬取的內容加入到 DataFrame 的 "content" 欄位
df['content'] = contents

# 將更新後的資料存回 Excel
df.to_excel(target_file, index=False)
