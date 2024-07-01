import praw
import csv
import os
from dotenv import load_dotenv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables from .env file
load_dotenv()

# Set up Reddit API credentials
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent=os.getenv('USER_AGENT')
)

# Define the subreddit and threshold
subreddit_name = 'AmItheAsshole'

# Function to determine the verdict from the comment
def get_verdict_from_comment(comment_body):
    comment_body = comment_body.lower()
    if 'yta' in comment_body:  # 'YTA' stands for "You're The Asshole"
        return 'YTA'
    elif 'nta' in comment_body:  # 'NTA' stands for "Not The Asshole"
        return 'NTA'
    elif 'esh' in comment_body:  # 'ESH' stands for "Everyone Sucks Here"
        return 'ESH'
    elif 'nah' in comment_body:  # 'NAH' stands for "No Assholes Here"
        return 'NAH'
    else:
        return 'N/A'  # In case the comment does not clearly state any known verdict

# Function to convert Unix timestamp to a readable date and time format
def convert_timestamp(timestamp):
    dt = datetime.utcfromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# Function to process a single post
def process_post(post):
    post.comments.replace_more(limit=0)  # Fetch all comments
    if len(post.comments) > 0:
        top_comment = post.comments[1]  # Get the topmost comment
        verdict = get_verdict_from_comment(top_comment.body)
        if verdict is not None:
            date_time = convert_timestamp(post.created).split()
            return {
                'post_id': post.id,
                'score': post.score,
                'top_comment_id': top_comment.id,
                'verdict': verdict,
                'date': date_time[0],  # Date part
                'time': date_time[1]  # Time part
            }
    return None

# Fetch top posts from the subreddit for the past year
subreddit = reddit.subreddit(subreddit_name)
posts = list(subreddit.top(time_filter='year', limit=1000))  # Adjust the time_filter as needed

print(f"Number of posts retrieved: {len(posts)}")  # Debugging statement

# Open the CSV file in write mode initially to write the header
with open('aita_results.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['post_id', 'score', 'top_comment_id', 'verdict', 'date', 'time'])
    writer.writeheader()

# Use ThreadPoolExecutor to process posts concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_post, post) for post in posts]
    with open('aita_results.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['post_id', 'score', 'top_comment_id', 'verdict', 'date', 'time'])
        for future in as_completed(futures):
            result = future.result()
            if result:
                writer.writerow(result)

print(f"Results have been written to aita_results.csv")
