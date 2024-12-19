import os
from crawler.crawler import main as crawler
from filter.filter import main as filter
from bedrock.bedrock import main as bedrock
import time

def ensure_directory(path):
    # make share the directory exit
    if not os.path.exists(path):
        os.makedirs(path)
        print ("Folder made")
    else:
        print("Folder already exit")

def main():
    articles_dir = "./articles"
    ensure_directory(articles_dir)

    # # 1st step: Crawler
    # print("\n Data Crawlering...")
    # crawler()
    # time.sleep(3)

    # # 2nd Step: Filter
    # print("\n Filtering ...")
    # filter()
    # time.sleep(3)

    # 3rd Srep: Summary
    print("\n Summarizing...")
    bedrock()
    


if __name__ == "__main__":
    main()
