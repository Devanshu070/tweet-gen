from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

def llm_config():
    """
        Fetches the provider from .env file and appropriately returns client,model
    """
    llm_provider = os.getenv("LLM_PROVIDER").lower()

    if llm_provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY in enviornemnt variables")
        client = OpenAI(api_key=api_key, base_url= "https://api.groq.com/openai/v1")
        model="openai/gpt-oss-20b"
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY in enviornemnt variables")
        client = OpenAI(api_key=api_key)
        model="gpt-4o-mini"
    
    return client, model


if __name__ == '__main__':
    client, model = llm_config()
    response = client.chat.completions.create(
        model = model,
        messages=[{'role':'user','content':'calculate 4+5'}]
    )
    print(response.choices[0].message.content)