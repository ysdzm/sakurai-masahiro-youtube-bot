import os
from googleapiclient.discovery import build

def get_api_key():
    api_key = os.environ.get('API_KEY')
    if not api_key:
        raise ValueError('YouTube API key not found in environment variables.')
    return api_key

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

    # 結果の処理
    videos = []
    for item in response['items']:
        video = {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
            'thumbnail_url': item['snippet']['thumbnails']['default']['url']
        }
        videos.append(video)

    return videos

# APIキーを取得
api_key = get_api_key()

# チャンネルIDを指定
channel_id = 'UC1EB8moGYdkoZQfWHjh7Ivw'

# 新着動画を取得
new_videos = get_new_videos(api_key, channel_id)

# 新着動画の情報を出力
for video in new_videos:
    print('Title:', video['title'])
    print('Video ID:', video['video_id'])
    print('Thumbnail URL:', video['thumbnail_url'])
    print('---')
