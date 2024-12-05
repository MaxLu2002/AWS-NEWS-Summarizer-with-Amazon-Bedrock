import pandas as pd
import requests
from bs4 import BeautifulSoup
import var
from datetime import datetime

# 英文檔案為目標
target_date = var.ENG_target_date
target_file = f'./articles/ENG_content_{target_date}.xlsx'

# 中文檔案為目標
# target_date = var.CHT_target_date
# target_file = f'./articles/CHT_content_{target_date}.xlsx'

# 讀取 Excel 檔案
df = pd.read_excel(target_file)
links = df['URL']
links = df['URL'].apply(lambda x: x.replace('aws.amazon.com/about-aws', 'aws.amazon.com/tw/about-aws'))

# 初始化空的內容列表
contents = []
titles = []
dates = []

# 依次訪問每個連結並爬取內文
for link in links:
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 爬取指定標籤的內文
        content_tags = soup.find_all('div', class_='wn-body')
        content = content_tags[1].get_text(strip=True) if len(content_tags) > 1 else ''
        
        title_tags = soup.find ('h1', class_="wn-title")
        title = title_tags.get_text(strip=True)
        
        date = content_tags[0].get_text(strip=True) if len(content_tags) > 1 else ''
        date_str = date.replace('Posted on:', '').strip()
        date_obj = datetime.strptime(date_str, '%b %d, %Y')  # 依據原始格式進行解析
        date = date_obj.strftime('%Y/%m/%d')  # 按照要求格式化為 "YYYY/MM/DD"
        
    except requests.RequestException as e:
        content = f'Error: {e}'
    contents.append(content)
    dates.append(date)
    titles.append(title)
    print (f"{link}爬取完成")

# 將爬取的內容加入到 DataFrame 的 "content" 欄位
df['Content'] = contents
df['Date'] = dates
df['Title'] = titles
# 將更新後的資料存回 Excel
df.to_excel(target_file, index=False)
