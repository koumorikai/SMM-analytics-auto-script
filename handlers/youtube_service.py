import requests
from conf.config import YOUTUBE_API_KEY, YOUTUBE_CHANNEL_ID

def fetch_youtube_metrics():
    """
    Забирает статистику YouTube-канала через официальный YouTube Data API v3.
    """
    print("Запрос данных из YouTube Data API...")
    
    if not YOUTUBE_API_KEY or not YOUTUBE_CHANNEL_ID:
        print("YouTube API Key не настроен. Используем тестовые данные.")
        return {"date": "2026-10", "followers_growth": 120, "reach": 15000, "impressions": 22000, "likes": 950}

    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "statistics",
        "id": YOUTUBE_CHANNEL_ID,
        "key": YOUTUBE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "items" in data and len(data["items"]) > 0:
            stats = data["items"][0]["statistics"]
            metrics = {
                "date": "2026-10",
                "followers_growth": int(stats.get("subscriberCount", 0)), # Общие подписчики 
                "reach": int(stats.get("viewCount", 0)),                
                "impressions": int(stats.get("viewCount", 0)),
                "likes": 0 
            }
            return metrics
    except Exception as e:
        print(f"Ошибка YouTube API: {e}")
        
    return {"date": "2026-10", "followers_growth": 0, "reach": 0, "impressions": 0, "likes": 0}