import praw
import re
from collections import Counter
from datetime import datetime, timedelta

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="AITA_Historical_Analysis_Bot v1.0 by YourUsername"
)

def analyze_aita_history(subreddit_name, days_to_analyze=30):
    subreddit = reddit.subreddit(subreddit_name)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days_to_analyze)
    
    post_verdicts = []
    overall_stats = Counter()

    for post in subreddit.new(limit=None):
        if post.created_utc < start_date.timestamp():
            break

        verdict = get_post_verdict(post)
        post_verdicts.append((post.title, verdict))
        overall_stats[verdict] += 1

    return post_verdicts, overall_stats

def get_post_verdict(post):
    post.comments.replace_more(limit=0)
    top_comments = sorted(post.comments, key=lambda x: x.score, reverse=True)[:10]
    
    vote_counter = Counter()
    for comment in top_comments:
        vote = extract_vote(comment.body)
        if vote:
            vote_counter[vote] += 1
    
    if not vote_counter:
        return "No Verdict"
    
    return vote_counter.most_common(1)[0][0]

def extract_vote(comment_body):
    vote_patterns = {
        'YTA': r'\bYTA\b',
        'NTA': r'\bNTA\b',
        'ESH': r'\bESH\b',
        'NAH': r'\bNAH\b',
        'INFO': r'\bINFO\b'
    }

    for vote, pattern in vote_patterns.items():
        if re.search(pattern, comment_body, re.IGNORECASE):
            return vote
    return None

if __name__ == "__main__":
    post_verdicts, overall_stats = analyze_aita_history("AmItheAsshole", days_to_analyze=30)
    
    print("Individual Post Verdicts:")
    for title, verdict in post_verdicts:
        print(f"Post: {title[:50]}... | Verdict: {verdict}")
    
    print("\nOverall Statistics:")
    total_posts = sum(overall_stats.values())
    for verdict, count in overall_stats.items():
        percentage = (count / total_posts) * 100
        print(f"{verdict}: {count} ({percentage:.2f}%)")