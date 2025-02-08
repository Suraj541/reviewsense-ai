import requests
import os

def fetch_tweets(query: str):
    headers = {"Authorization": f"Bearer {os.getenv('TWITTER_BEARER_TOKEN')}"}
    params = {
        "query": f"{query} -is:retweet",
        "tweet.fields": "created_at,public_metrics",
        "max_results": 10
    }
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/recent",
        headers=headers,
        params=params
    )
    return response.json()

def fetch_instagram_comments(media_id: str):
    params = {
        "access_token": os.getenv("INSTAGRAM_ACCESS_TOKEN"),
        "fields": "timestamp,text,username"
    }
    response = requests.get(
        f"https://graph.instagram.com/{media_id}/comments",
        params=params
    )
    return response.json()