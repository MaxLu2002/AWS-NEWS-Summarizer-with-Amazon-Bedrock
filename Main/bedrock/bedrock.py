import boto3
import json
import pandas as pd
import time
import config


# 模組：生成提示詞
def generate_question(content,language):
    """Identify your prompt"""
    question = """
        Act as a summarizer specializing in AWS technical articles. Your task is to summarize {CONTENT} following the specified "RULES" and "format":

        "RULES"
        1. Always respond in {language}.
        2. Provide information in 1-3 bullet points.
        3. Each bullet point should be 1-2 sentences, written in a way that is clear for engineers to understand.
        4. Summarize each article according to the "format" in {language}.

        "format"    
        --The Problem--
        1. 
        2. 
        3.
        
        --How this solution solved it--
        1. 
        2. 
        3.
    """
    return question.format(CONTENT=content,language=language)

# module of API Request
def prepare_api_parameters(question):
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
                            "text": question
                        }
                    ]
                }
            ]
        })
    }

def call_bedrock_api(client, kwargs):
    response = client.invoke_model(**kwargs)
    body = json.loads(response['body'].read())
    return body["content"][0]['text']

def update_dataframe_with_summary(df, client,language):    
    for index, row in df.iterrows():
        content = row['Content']
        question = generate_question(content,language)
        kwargs = prepare_api_parameters(question)
        summary = call_bedrock_api(client, kwargs)

        df.at[index, "Summarize"] = summary
        print("\n", summary)
        time.sleep(1)

    

# 主函式
def main():
    target_date = config.target_date
    language = config.language
    file_name = f"ENG_content_{target_date}"
    file_path = f"./articles/{file_name}.xlsx"
    df = pd.read_excel(file_path)
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    
    update_dataframe_with_summary(df, client, language)
    
    df.to_excel(file_path, index=False)

if __name__ == "__main__":
    main()