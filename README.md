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
    export AWS_PROFILE=your_profile_name 
    ```

4. Configure the ChromeDriver path:
    In `1_crawler_ENG.py`, modify the following path to your local ChromeDriver path:
    ```python
    service = Service("C:/downloads/chromedriver-win64/chromedriver.exe")
    ```

## Usage Instructions

### 1. set the time variable in "config.py", this is the date that you will crawler. e.g. if equal to "1212", the crawler will scrape til 12 december 

### 2. set the environment variable in terminal , you need to identity AWS bedrock access through aws configure e.g. $env:AWS_PROFILE="YOUR-PROFILE-NAME"

### 3. apply main.py
