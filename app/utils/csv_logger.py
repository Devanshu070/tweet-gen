import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.abspath(os.path.join(current_dir,'..','..'))
# assuming data folder exists in root dir
file_path = os.path.join(project_root_dir,'data','tweets_audits.csv')



def init_csv():
    # if DB file doesn't exists create one

    if not os.path.exists(file_path):
        with open(file_path, mode='w',newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'draft_id', 'event_id','timestamp','prompt', 'tweet', 'feedback', 'action']) 


def append_tweet_data(*, user_id, draft_id, event_id, prompt, tweet, action, feedback=''):
    IST = ZoneInfo("Asia/Kolkata")
    timestamp = datetime.now(IST).isoformat()
    # print(timestamp)

    with open(file_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([user_id, draft_id, event_id, timestamp, prompt, tweet, feedback, action])

if __name__ == "__main__":
    init_csv()