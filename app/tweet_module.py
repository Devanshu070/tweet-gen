from openai import OpenAI
from config import llm_config

client, model = llm_config()


def generate_tweet(prompt: str) -> str:
    response = client.chat.completions.create(
        model = model,
        messages=[{'role':'user', 'content' : prompt}]
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    response=generate_tweet("hi, caluclate 1+3")
    print(response)