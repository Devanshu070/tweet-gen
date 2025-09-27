from app.config import llm_config
from app.prompts import tweet_generator_prompt

client, model = llm_config()


def generate_tweet(prompt: str) -> str:
    template = tweet_generator_prompt()
    formated_prompt = template.format(prompt=prompt)

    response = client.chat.completions.create(
        model = model,
        messages=[{'role':'user', 'content' : formated_prompt}]
    )
    return response.choices[0].message.content

# def generate_tweet_with_feedback(prompt:str, tweet:str, feedback:str) ->str:
#     template = 

if __name__ == '__main__':
    # to run file for debugging
    # uv run -m app.tweet_generator
    response=generate_tweet("hi generate a tweet on AI boom. also discuss the devlopments taking plcae in india")
    print(response)