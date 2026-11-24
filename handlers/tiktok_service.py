import os
import requests
import yt_dlp


def _fetch_via_rapidapi(username: str) -> dict | None:
    """Пробует получить метрики TikTok через RapidAPI, если заданы ключ и хост."""
    api_key = os.getenv("RAPIDAPI_KEY")
    api_host = os.getenv("RAPIDAPI_TIKTOK_HOST")
    endpoint_url = os.getenv("RAPIDAPI_TIKTOK_URL")

    if not api_key or not api_host or not endpoint_url:
        return None

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host,
    }
    response = requests.get(
        endpoint_url,
        headers=headers,
        params={"username": username},
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    recent_posts = data.get("videos", [])
    total_views = sum(v.get("views", 0) for v in recent_posts)
    total_likes = sum(v.get("likes", 0) for v in recent_posts)
    total_comments = sum(v.get("comments", 0) for v in recent_posts)
    total_shares = sum(v.get("shares", 0) for v in recent_posts)

    posts_count = len(recent_posts)
    avg_views = round(total_views / posts_count, 2) if posts_count > 0 else 0.0
    total_engagements = total_likes + total_comments + total_shares
    er_rate = round((total_engagements / total_views * 100), 2) if total_views > 0 else 0.0

    return {
        "platform": "TikTok",
        "username": username,
        "followers": data.get("followers_count", 0),
        "posts_analyzed": posts_count,
        "views": total_views,
        "avg_views": avg_views,
        "likes": total_likes,
        "comments": total_comments,
        "shares": total_shares,
        "er_rate": er_rate,
    }


def _fetch_via_ytdlp(username: str, limit: int = 10) -> dict:
    """Резервный сбор метрик последних видео профиля через yt-dlp."""
    clean_user = username.lstrip("@")
    url = f"https://www.tiktok.com/@{clean_user}"
    ydl_opts = {
        "quiet": True,
        "extract_flat": False,
        "playlistend": limit,
        "ignoreerrors": True,
    }

    total_views = 0
    total_likes = 0
    total_comments = 0
    total_shares = 0
    posts_count = 0

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        entries = info.get("entries", []) if info else []

        for video in entries:
            if not video:
                continue
            total_views += video.get("view_count") or 0
            total_likes += video.get("like_count") or 0
            total_comments += video.get("comment_count") or 0
            total_shares += video.get("repost_count") or video.get("share_count") or 0
            posts_count += 1

    avg_views = round(total_views / posts_count, 2) if posts_count > 0 else 0.0
    total_engagements = total_likes + total_comments + total_shares
    er_rate = round((total_engagements / total_views * 100), 2) if total_views > 0 else 0.0

    return {
        "platform": "TikTok",
        "username": clean_user,
        "followers": 0,
        "posts_analyzed": posts_count,
        "views": total_views,
        "avg_views": avg_views,
        "likes": total_likes,
        "comments": total_comments,
        "shares": total_shares,
        "er_rate": er_rate,
    }


def fetch_tiktok_metrics(username: str = "example_user") -> dict:
    """Основная точка входа: сначала пробует RapidAPI, при отсутствии ключа — yt-dlp."""
    print(f"Запрос данных TikTok для: @{username.lstrip('@')}")
    try:
        rapid_data = _fetch_via_rapidapi(username)
        if rapid_data is not None:
            return rapid_data
        return _fetch_via_ytdlp(username)
    except Exception as e:
        print(f"Ошибка при сборе статистики TikTok (@{username}): {e}")
        return {
            "platform": "TikTok",
            "username": username.lstrip("@"),
            "followers": 0,
            "posts_analyzed": 0,
            "views": 0,
            "avg_views": 0.0,
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "er_rate": 0.0,
        }