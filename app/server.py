from enum import Enum
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from app.tweet_generator import generate_tweet
from app.utils.csv_logger import init_csv, append_tweet_data
from uuid import uuid4

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, this is the root page"}


class TweetAction(str, Enum):
    """Enumeration of actions representing the tweet content lifecycle."""
    original_draft = "original_draft"            # first tweet generated for the given prompt
    re_generated = "re_generated"                # fresh tweet generated again for the same input/prompt
    edited = "edited"                            # user manually edits the tweet
    tweet_with_feedback = "tweet_with_feedback"    # user provides feedback so LLM generates new tweet accordingly
    published = "published"                      # final tweet is published/posted


class tweet_request(BaseModel):
    
    """Request body for generating a tweet from a user-provided prompt."""

    user_id: str= Field(..., description='Unique user_id assigned to an individual user')
    draft_id: str= Field(..., description='Unique draft_id assigned to a draft')
    prompt: str = Field(..., description='Input given by the user to generate tweet')

    @field_validator('user_id')
    def validate_user_id(cls, v):
        if not v.strip():
            raise ValueError('User id cannot be empty')
        return v

    @field_validator('draft_id')
    def validate_draft_id(cls, v):
        if not v.strip():
            raise ValueError('Draft id cannot be empty')
        return v

    @field_validator('prompt')
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValueError("Input cannot be empty")
        return v


class tweet_event_input(tweet_request):
    tweet: str =Field(..., description= 'Tweet')

    @field_validator('tweet')
    def validate_tweet(cls,v):
        if not v.strip():
            raise ValueError("Tweet cannot be empty")
        return v   


class publish_event_input(tweet_event_input):
    event_id: str = Field(..., description='Event id of the last event occured')

    @field_validator('event_id')
    def validate_tweet(cls,v):
        if not v.strip():
            raise ValueError("Event_id cannot be empty")
        return v  

class tweet_with_feedback(tweet_event_input):
    feedback: str = Field(..., description='Feedback given by the user to optimize the tweet')

    @field_validator('feedback')
    def validate_tweet(cls,v):
        if not v.strip():
            raise ValueError("Feedback cannot be empty")
        return v  


@app.post('/generate')
def generate_tweet_helper(input: tweet_request) -> dict:
    init_csv()
    tweet = generate_tweet(input.prompt)
    event_id = str(uuid4())
    append_tweet_data(user_id=input.user_id, draft_id=input.draft_id, prompt=input.prompt, tweet= tweet, event_id=event_id, action=TweetAction.original_draft.value)

    return {'tweet':tweet, 'draft_id':input.draft_id, 'event_id':event_id}

@app.post('/edit')
def edit_generated_tweet_helper(input: tweet_event_input) -> dict:
    # we input the edited tweet and save it into our csv
    event_id = str(uuid4())
    append_tweet_data(user_id= input.user_id, prompt=input.prompt, tweet= input.tweet, draft_id=input.draft_id, event_id=event_id, action=TweetAction.edited.value)
    return {'tweet':input.tweet, 'draft_id':input.draft_id, 'event_id':event_id}

@app.post('/re_generate')
def generate_tweet_helper(input: tweet_request) -> dict:
    init_csv()
    tweet = generate_tweet(input.prompt)
    event_id = str(uuid4())
    append_tweet_data(user_id=input.user_id, draft_id=input.draft_id, prompt=input.prompt, tweet= tweet, event_id=event_id, action=TweetAction.re_generated.value)

    return {'tweet':tweet, 'draft_id':input.draft_id, 'event_id':event_id}

@app.post('/tweet_with_feedback')
def tweet_with_feedback_helper(input: tweet_with_feedback) -> dict:
    old_tweet = input.tweet
    feedback = input.feedback
    new_tweet = f'function to be initialized and improted, giving fn input {old_tweet},{feedback }'
    event_id = str(uuid4())
    append_tweet_data(user_id=input.user_id, draft_id=input.draft_id, prompt=input.prompt, tweet= new_tweet, event_id=event_id, feedback=input.feedback, action=TweetAction.tweet_with_feedback.value)
    return {'tweet':new_tweet, 'draft_id':input.draft_id, 'event_id':event_id}

@app.post('/publish')
def publish_tweet_helper(input: publish_event_input) -> dict:
    publish_event_id = input.event_id
    
    # retrieving tweet for the tweet to be published with help of event_id
    
    # add publish funcitonality here


    current_event_id = str(uuid4())
    append_tweet_data(user_id= input.user_id, prompt=input.prompt, tweet= input.tweet, draft_id=input.draft_id, event_id=current_event_id, action=TweetAction.published.value)
    return {'tweet':input.tweet, 'draft_id':input.draft_id, 'event_id':current_event_id}