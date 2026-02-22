#!/usr/bin/env python3
"""
Auto-post blog updates to Twitter/X and Line OA
"""

import os
import json
import requests
import tweepy
from datetime import datetime

# Configuration
BLOG_PLAN_FILE = "blog-content-plan.json"
WEBSITE_URL = "https://www.nc-story.com"

# API Credentials (from environment variables)
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
LINE_CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")


def get_latest_blog_post():
    """Get the most recently completed blog post"""
    with open(BLOG_PLAN_FILE, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    if not plan.get('completed'):
        return None

    # Get the last completed post
    latest = plan['completed'][-1]
    return latest


def create_tweet_text(post):
    """Create engaging tweet text"""
    title = post['title']
    slug = post.get('generated_slug', '')
    url = f"{WEBSITE_URL}/blog/{slug}"

    # Create tweet (max 280 chars including URL)
    tweet = f"""🔥 บทความใหม่!

{title}

อ่านฟรีที่ 👇
{url}

#นิยายไทย #นิยายNC #DarkRomance #อ่านนิยาย"""

    # Ensure within Twitter's limit
    if len(tweet) > 280:
        # Truncate title if needed
        max_title_len = 280 - len(tweet) + len(title) - 3
        title_short = title[:max_title_len] + "..."
        tweet = f"""🔥 บทความใหม่!

{title_short}

อ่านฟรีที่ 👇
{url}

#นิยายไทย #นิยายNC"""

    return tweet


def create_line_message(post):
    """Create Line message"""
    title = post['title']
    slug = post.get('generated_slug', '')
    url = f"{WEBSITE_URL}/blog/{slug}"

    message = f"""📚 มีบทความใหม่แล้วค่ะ!

{title}

✨ อ่านฟรีที่
{url}

#นิยายไทย #นิยายNC #DarkRomance"""

    return message


def post_to_twitter(tweet_text):
    """Post to Twitter/X"""
    try:
        # Authenticate with Twitter API v2
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )

        # Create tweet
        response = client.create_tweet(text=tweet_text)
        print(f"✅ Posted to Twitter: Tweet ID {response.data['id']}")
        return True

    except Exception as e:
        print(f"❌ Twitter error: {e}")
        return False


def post_to_line(message_text):
    """Broadcast to all Line OA followers"""
    try:
        url = "https://api.line.me/v2/bot/message/broadcast"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_CHANNEL_TOKEN}"
        }

        payload = {
            "messages": [
                {
                    "type": "text",
                    "text": message_text
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print("✅ Posted to Line OA")
            return True
        else:
            print(f"❌ Line error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Line error: {e}")
        return False


def main():
    """Main function"""
    print("🤖 Starting social media auto-post...")

    # Check if credentials are set
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET,
                TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
        print("⚠️  Twitter credentials not found. Skipping Twitter.")
        twitter_enabled = False
    else:
        twitter_enabled = True

    if not LINE_CHANNEL_TOKEN:
        print("⚠️  Line credentials not found. Skipping Line.")
        line_enabled = False
    else:
        line_enabled = True

    if not twitter_enabled and not line_enabled:
        print("❌ No social media credentials configured. Exiting.")
        return

    # Get latest blog post
    latest_post = get_latest_blog_post()
    if not latest_post:
        print("ℹ️  No blog posts found. Nothing to post.")
        return

    print(f"📝 Latest post: {latest_post['title']}")

    # Post to Twitter
    if twitter_enabled:
        tweet_text = create_tweet_text(latest_post)
        print(f"\n📱 Tweet preview:\n{tweet_text}\n")
        post_to_twitter(tweet_text)

    # Post to Line
    if line_enabled:
        line_message = create_line_message(latest_post)
        print(f"\n💬 Line message preview:\n{line_message}\n")
        post_to_line(line_message)

    print("\n✅ Social media posting complete!")


if __name__ == "__main__":
    main()
