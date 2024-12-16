import boto3
import json
import pandas as pd
import time
import config

# 模組：讀取檔案
def read_file(file_path):
    """read excel file"""
    return pd.read_excel(file_path)

# 模組：初始化 Bedrock Runtime 客戶端
def initialize_bedrock_client(region="us-east-1"):
    """init Bedrock Runtime"""
    return boto3.client("bedrock-runtime", region_name=region)

# 模組：生成提示詞
def generate_prompt(content):
    """Identify your prompt"""
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
    return prompt_template.format(CONTENT=content)

# module of API Request
def prepare_api_parameters(prompt):
    return {
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

def call_bedrock_api(client, kwargs):
    """呼叫 Bedrock API 並返回回應。"""
    response = client.invoke_model(**kwargs)
    body = json.loads(response['body'].read())
    return body["content"][0]['text']

def update_dataframe_with_summary(df, client):
    """遍歷 DataFrame 並用摘要更新。"""
    for index, row in df.iterrows():
        content = row['Content']
        prompt = generate_prompt(content)
        kwargs = prepare_api_parameters(prompt)
        summary = call_bedrock_api(client, kwargs)

        df.at[index, "Summarize"] = summary
        print("\n", summary)
        time.sleep(1)

def save_to_excel(df, file_path):
    """將 DataFrame 保存回 Excel 檔案。"""
    df.to_excel(file_path, index=False)

# 主函式
def main():
    target_date = config.target_date
    file_name = f"ENG_content_{target_date}"
    file_path = f"./articles/{file_name}.xlsx"

    df = read_file(file_path)
    client = initialize_bedrock_client()
    update_dataframe_with_summary(df, client)
    save_to_excel(df, file_path)

if __name__ == "__main__":
    main()
