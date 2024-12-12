# AWS Article Scraper and Summarizer

本專案是一個自動化工具，用於爬取 AWS 官方網站的技術文章，過濾並篩選內容，並生成簡單摘要以供工程師快速閱讀和使用。

## 功能特性

1. **爬取內容**：透過 Selenium 爬取 AWS 網站的最新文章資料，包括標題、發佈日期和連結。
2. **內容篩選**：利用 BeautifulSoup 和 pandas 進行文章內容的提取與日期篩選。
3. **摘要生成**：使用 AWS Bedrock 的自然語言處理模型生成文章的摘要。
4. **儲存輸出**：將篩選後的文章及其摘要儲存到 Excel 檔案中，方便後續查看。

## 環境需求

- Python 3.7+
- Chrome 瀏覽器及相應版本的 ChromeDriver
- 已安裝並設定 AWS CLI
- 必要的 Python 套件 (請參考下方安裝指引)

## 安裝指引

1. 安裝必要的 Python 套件：
    ```bash
    pip install selenium pandas requests beautifulsoup4 boto3 openpyxl
    ```

2. 確保 AWS CLI 已設定：
    ```bash
    aws configure
    ```
    **注意**：請確保 AWS 帳戶具備使用 Bedrock API 的權限。

3. 設定環境變數(e.g. on PowerShell)：
    ```bash
    export AWS_PROFILE=your_profile_name 
    ```

4. 設定 ChromeDriver 的路徑：
    在 `1_crawler_ENG.py` 中，修改以下路徑為您本機的 ChromeDriver 路徑：
    ```python
    service = Service("C:/下載程式/chromedriver-win64/chromedriver.exe")
    ```

## 使用說明

### 1. 設定日期
在 `config.py` 中修改目標日期 `target_date` (格式：YYYYMMDD)：
    ```python
    target_date = "20241211"
    '''

### 2. 爬取 AWS 網站文章

執行 1_crawler_ENG.py：

python 1_crawler_ENG.py

此步驟將爬取文章並將資料儲存至 ./articles/ENG_content_<target_date>.xlsx。

---

### 3. 篩選與提取內容

執行 2_filter_ENG.py：

python 2_filter_ENG.py

此步驟會提取每篇文章的內容、標題和發佈日期，並篩選符合目標日期的文章。

---

### 4. 生成摘要

執行 3_bedrock-SUM.py：

python 3_bedrock-SUM.py

此步驟將利用 AWS Bedrock API 為篩選後的文章生成摘要，並更新至 Excel 檔案。

---

### 輸出結果

篩選後的文章將儲存在 ./articles/ENG_content_<target_date>.xlsx。每篇文章包含以下欄位：

Title：文章標題
Date：文章日期
URL：文章連結
Content：文章全文
Summarize：文章摘要

---

### 注意事項

ChromeDriver：請確保 ChromeDriver 版本與 Chrome 瀏覽器相符，否則可能導致錯誤。
AWS API：執行摘要生成時需具備 AWS Bedrock API 的存取權限。
Excel 檔案存取：若檔案被其他應用程式開啟，可能導致存取失敗。
