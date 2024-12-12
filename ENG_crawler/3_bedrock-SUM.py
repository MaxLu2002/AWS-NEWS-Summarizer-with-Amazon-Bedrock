import boto3
import json
import pandas as pd
import time
import config

# Read the specified file
target_date = config.target_date
file_name = f"ENG_content_{target_date}"
file_path = f"./articles/{file_name}.xlsx"

# Initialize Bedrock Runtime client
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")
# Execute the following to set environment variables
    # $env:AWS_PROFILE="your-profile"
    # aws s3 ls (check)

# Define bot prompt
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

# Iterate through the "Content" column in each row of the Excel file
for index, row in df.iterrows():
    content = row['Content']
    prompt = prompt_template.format(CONTENT=content)

    # Prepare API request parameters
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

    # Call Bedrock API
    response = bedrock_runtime.invoke_model(**kwargs)
    body = json.loads(response['body'].read())
    summary = body["content"][0]['text']

    # Save the summary result back to the "Summarize" column
    df.at[index, "Summarize"] = summary

    # Output the summary result
    print("\n", summary)
    time.sleep(1)

df.to_excel(file_path, index=False)