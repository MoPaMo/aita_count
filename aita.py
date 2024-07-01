import praw
import csv
from dotenv import load_dotenv
import os

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
vote_threshold = 1000  # Define your vote threshold here

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
        return None  # In case the comment does not clearly state any known verdict

# Fetch posts from the subreddit
subreddit = reddit.subreddit(subreddit_name)
posts = subreddit.search('score:>1000', limit=1000)  # You can adjust the limit as needed

# Open the CSV file in write mode initially to write the header
with open('aita_results.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['post_id', 'score', 'top_comment_id', 'verdict', 'date'])
    writer.writeheader()

# Open the CSV file in append mode to write each row
with open('aita_results.csv', mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['post_id', 'score', 'top_comment_id', 'verdict', 'date'])
    
    for post in posts:
        if post.score >= vote_threshold:
            post.comments.replace_more(limit=0)  # Fetch all comments
            if len(post.comments) > 0:
                top_comment = post.comments[0]  # Get the topmost comment

                verdict = get_verdict_from_comment(top_comment.body)
                if verdict is not None:
                    writer.writerow({
                        'post_id': post.id,
                        'score': post.score,
                        'top_comment_id': top_comment.id,
                        'verdict': verdict,
                        'date': post.created
                    })

print(f"Results have been written to aita_results.csv")
