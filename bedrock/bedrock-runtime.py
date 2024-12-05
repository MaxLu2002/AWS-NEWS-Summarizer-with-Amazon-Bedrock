import boto3
import json
import pandas as pd
import time

# 初始化 Bedrock Runtime 客戶端
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

# 定義機器人Prompt
prompt_template = """
  Act as a summarizer specializing in AWS technical articles. Your task is to condense each article into a single concise sentence that captures the core idea and key information. Ensure the summaries are clear, accurate, and easy to understand.
  and you will always answer in Traditional Chinese
  
  Article content:
  {CONTENT}
"""

# 讀取Excel文件
file_path = "./articles/ENG_content_20241203.xlsx"
save_path = "./bedrock/sum_result/ENG_content_20241203.xlsx"

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
            "max_tokens": 250,
            "top_k": 350,
            "stop_sequences": [],
            "temperature": 1,
            "top_p": 0.5,
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
    df.at[index, "SUM"] = summary

    # 輸出摘要結果
    print("\n", summary)
    time.sleep(1)


df.to_excel(save_path, index=False)
