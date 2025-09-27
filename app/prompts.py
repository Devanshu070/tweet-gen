from langchain_core.prompts import PromptTemplate

def tweet_generator_prompt() :
    formateed_prompt = PromptTemplate(
        template="""You are a creative social media assistant.
        Your task is to generate a tweet for X(formerly twitter) on the input "{prompt}".
        - Keep the tweet under 280 characters.
        - Make it engaging, natural, and suitable for Twitter.
        - Use emojis and hashtags where appropriate.
        """,
        input_variables=['prompt']
    )
    return formateed_prompt

