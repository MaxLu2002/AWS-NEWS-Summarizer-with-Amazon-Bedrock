# AWS Article Scraper and Summarizer

This project is an automated tool designed to scrape technical articles from the official AWS website, filter and process the content, and generate concise summaries for engineers to read and utilize quickly.

## Features

1. **Content Scraping**: Uses Selenium to scrape the latest article data from the AWS website, including titles, publication dates, and links.
2. **Content Filtering**: Extracts and filters article content and dates using BeautifulSoup and pandas.
3. **Summary Generation**: Utilizes AWS Bedrock's natural language processing model to generate article summaries.
4. **Output Storage**: Saves the filtered articles and their summaries to an Excel file for easy review.

## Requirements

- Python 3.7+
- Chrome browser and the corresponding version of ChromeDriver
- AWS CLI installed and configured
- Required Python libraries (refer to the installation guide below)

## Installation Guide

1. Install the required Python libraries:
    ```bash
    pip install selenium pandas requests beautifulsoup4 boto3 openpyxl
    ```

2. Ensure AWS CLI is configured:
    ```bash
    aws configure
    ```
    **Note**: Make sure your AWS account has permissions to use the Bedrock API.

3. Set environment variables (e.g., on PowerShell):
    ```bash
    $env:AWS_PROFILE="intern"
    ```

4. Configure the ChromeDriver path:
    In `1_crawler_ENG.py`, modify the following path to your local ChromeDriver path:
    ```python
    service = Service("C:/downloads/chromedriver-win64/chromedriver.exe")
    ```

## Usage Instructions


### 1. Configure Variables
Set the `time` and `language` variables in the `config.py` file. The `time` variable represents the target date for the web crawler, while the `language` variable specifies the language for the output. For example:
- If `time` is set to `1212`, the crawler will scrape data up to December 12th.
- If `language` is set to "Traditional Chinese", the output will be in Traditional Chinese.

### 2. Set Environment Variables
Configure the environment variable in your terminal to enable AWS Bedrock access. Use the AWS CLI to set your profile:

$env:AWS_PROFILE="YOUR-PROFILE-NAME"

Replace `YOUR-PROFILE-NAME` with the appropriate AWS profile name.

### 3. Run the Main Script
Execute the `main.py` script to start the process:

python main.py

The `main.py` script performs the following steps:
1. Crawls news titles, URLs, and dates using `crawler.py`.
2. Filters and processes the data using `filter.py`.
3. Summarizes the content of each article using Amazon Bedrock.

