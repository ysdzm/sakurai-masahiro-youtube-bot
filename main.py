import os
import requests
from googleapiclient.discovery import build

def get_api_key():
    api_key = os.environ.get('API_KEY')
    if not api_key:
        raise ValueError('YouTube API key not found in environment variables.')
    return api_key

def get_webhook_url():
    webhook_url = os.environ.get('WEBHOOK_URL')
    if not webhook_url:
        raise ValueError('Discord webhook URL not found in environment variables.')
    return webhook_url

def get_new_videos(api_key, channel_id, max_results=10):
    # YouTube Data APIのビルド
    youtube = build('youtube', 'v3', developerKey=api_key)

    # 新着動画を取得するリクエスト
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        order='date',
        type='video',
        maxResults=max_results
    )

    # APIリクエストの送信
    response = request.execute()

    # 動画の情報を取得
    videos = []
    for item in response['items']:
        video = {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
            'published_at': item['snippet']['publishedAt']
        }
        videos.append(video)

    return videos

def save_video_id(video_id, filename='latest_video_id.txt'):
    with open(filename, 'w') as f:
        f.write(video_id)

def get_latest_video_id(filename='latest_video_id.txt'):
    with open(filename, 'r') as f:
        return f.read().strip()

# APIキーを取得
api_key = get_api_key()

# 桜井政博のゲーム作るにはのチャンネルIDを指定
channel_id = 'UC5CTV3JSdrlo5Pa42QkK8SA'

# 最新の動画のVideo IDを取得
latest_video_id = get_latest_video_id()

# 最新の10件の動画を取得
new_videos = get_new_videos(api_key, channel_id)

# 最新の動画よりも古い動画のVideo IDを出力し、Video IDを更新
for video in new_videos:
    if video['video_id'] != latest_video_id:
        # Discordにメッセージを送信
        webhook_url = get_webhook_url()
        message = {
            "username": "桜井政博のゲーム作るにはbot", 
            "avatar_url": "https://yt3.googleusercontent.com/aoouNzNe8R3Blcmy8EghybnFbCsbexbjK6gBi6Mapli0xpt5r-mubIpODo1IGPr54eyULZs=s176-c-k-c0x00ffffff-no-rj", 
            "content": f"New video: {video['title']} - https://www.youtube.com/watch?v={video['video_id']}"
            }
        requests.post(webhook_url, json=message)
    else:
        break

# 最新の動画IDを更新
if new_videos:
    latest_video_id = new_videos[0]['video_id']
    save_video_id(latest_video_id)
