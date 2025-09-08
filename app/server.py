from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from app.tweet_generator import generate_tweet

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, this is the root page"}

class tweet_request(BaseModel):
    prompt: str = Field(..., description='Input given by the user to generate tweet')

    @field_validator('prompt')
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Input cannot be empty")
        return v

@app.post('/generate')
def generate_tweet_helper(input: tweet_request) -> dict:
    tweet = generate_tweet(input.prompt)
    return {'tweet':tweet}
    