import boto3
import json
import pandas as pd
import time
import config

# 讀取指定文件
target_date = config.target_date
file_name = f"ENG_content_{target_date}"
file_path = f"./articles/{file_name}.xlsx"

# 初始化 Bedrock Runtime 客戶端
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")
# 執行以下設定環境變數
    # $env:AWS_PROFILE="intern"
    # aws s3 ls (檢查)


# 定義機器人Prompt
prompt_template = """
    Act as a summarizer specializing in AWS technical articles. Your task is to summarize {CONTENT} following the specified "RULES" and "format":

    "RULES"
    1. Summarize each article according to the "format".
    2. Provide information in 1-3 bullet points.
    3. Each bullet point should be 1-2 sentences, written in a way that is clear for engineers to understand.
    4. Always respond in Traditional Chinese.

    "format"    
    --解決的問題--
    1. 
    2. 
    3.
    
    --解決的方式--
    1. 
    2. 
    3.

"""

df = pd.read_excel(file_path)

# 遍歷Excel中每一列的"Content"欄位
for index, row in df.iterrows():
    content = row['Content']
    prompt = prompt_template.format(CONTENT=content)

    # 準備API請求參數
    kwargs = {
        "modelId": "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "stop_sequences": [],
            "temperature": 1,
            "top_p": 0.5,
            "top_k": 100,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        })
    }

    # 調用 Bedrock API
    response = bedrock_runtime.invoke_model(**kwargs)
    body = json.loads(response['body'].read())
    summary = body["content"][0]['text']

    # 將摘要結果存回"SUM"欄位
    df.at[index, "Summarize"] = summary

    # 輸出摘要結果
    print("\n", summary)
    time.sleep(1)


df.to_excel(file_path, index=False)
