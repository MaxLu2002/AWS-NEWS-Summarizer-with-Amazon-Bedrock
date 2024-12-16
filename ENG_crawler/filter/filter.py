import pandas as pd
import requests
from bs4 import BeautifulSoup
import config
from datetime import datetime

def read_excel_file(target_file):
    """Read the Excel file and prepare links."""
    df = pd.read_excel(target_file)
    links = df['URL'].apply(lambda x: x.replace('aws.amazon.com/about-aws', 'aws.amazon.com/about-aws'))
    return df, links

def fetch_page_content(link):
    """Fetch page content, title, and date from a given URL."""
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract content
        content_tags = soup.find_all('div', class_='wn-body')
        content = content_tags[1].get_text(strip=True) if len(content_tags) > 1 else ''

        # Extract title
        title_tags = soup.find('h1', class_="wn-title")
        title = title_tags.get_text(strip=True)

        # Extract and format date
        date = content_tags[0].get_text(strip=True) if len(content_tags) > 1 else ''
        date_str = date.replace('Posted on:', '').strip()
        date_obj = datetime.strptime(date_str, '%b %d, %Y')
        date = date_obj.strftime('%Y/%m/%d')

    except requests.RequestException as e:
        content = f'Error: {e}'
        title = ''
        date = ''

    return content, title, date

def scrape_content(links):
    """Scrape content, titles, and dates from all links."""
    contents = []
    titles = []
    dates = []

    for link in links:
        content, title, date = fetch_page_content(link)
        contents.append(content)
        titles.append(title)
        dates.append(date)
        print(f"{link} Cleaned ")

    return contents, titles, dates

def save_to_excel(df, target_file, contents, titles, dates,target_date):
    df['Content'] = contents
    df['Date'] = dates
    df['Title'] = titles
    
    try:
        target_date = datetime.strptime(target_date, "%Y%m%d").date()
        rows_to_drop = []
        for index, row in df.iterrows():
            row_date = datetime.strptime(row['Date'], "%Y/%m/%d").date()
            
            if row_date < target_date:
                rows_to_drop.append(index)
        
        df_filtered = df.drop(rows_to_drop)
        df_filtered.to_excel(target_file, index=False)
        print(f"Data Saved to {target_file}")
        print(f"Data Rows：{len(df_filtered)}")
        
    except ValueError as e:
        print(f"Date Error：{e}")
    except Exception as e:
        print(f"Save Effor：{e}")

def main():
    target_date = config.target_date
    target_file = f'./articles/ENG_content_{target_date}.xlsx'

    # Read Excel file
    df, links = read_excel_file(target_file)

    # Scrape content
    contents, titles, dates = scrape_content(links)

    # Save updated content to Excel
    save_to_excel(df, target_file, contents, titles, dates,target_date)

if __name__ == "__main__":
    main()