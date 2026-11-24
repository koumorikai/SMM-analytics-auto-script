from datetime import datetime, timezone
import requests
from conf.config import INSTAGRAM_ACCOUNT_ID, INSTAGRAM_ACCESS_TOKEN


def _empty_metrics(date_str: str) -> dict:
    """Возвращает нулевую структуру метрик при ошибке запроса или отсутствии ключей."""
    return {
        "platform": "Instagram",
        "date": date_str,
        "followers": 0,
        "media_count": 0,
        "reach": 0,
        "impressions": 0,
        "likes": 0,
    }


def fetch_instagram_metrics() -> dict:
    """Запрашивает метрики аккаунта и последних публикаций из Instagram Graph API."""
    current_date = datetime.now(timezone.utc).strftime("%Y-%m")

    if not INSTAGRAM_ACCOUNT_ID or not INSTAGRAM_ACCESS_TOKEN:
        print("Не заданы INSTAGRAM_ACCOUNT_ID или INSTAGRAM_ACCESS_TOKEN в .env / conf.config.")
        return _empty_metrics(current_date)

    base_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}"

    try:
        # 1. Базовые показатели профиля
        profile_resp = requests.get(
            base_url,
            params={
                "fields": "username,followers_count,media_count",
                "access_token": INSTAGRAM_ACCESS_TOKEN,
            },
            timeout=15,
        )
        if profile_resp.status_code != 200:
            print(f"Ошибка API Instagram (profile {profile_resp.status_code}): {profile_resp.text}")
            return _empty_metrics(current_date)

        profile_data = profile_resp.json()
        followers = profile_data.get("followers_count", 0)
        media_count = profile_data.get("media_count", 0)

        # 2. Лайки по последним публикациям (до 25 постов)
        total_likes = 0
        media_resp = requests.get(
            f"{base_url}/media",
            params={
                "fields": "like_count,comments_count,timestamp",
                "limit": 25,
                "access_token": INSTAGRAM_ACCESS_TOKEN,
            },
            timeout=15,
        )
        if media_resp.status_code == 200:
            posts = media_resp.json().get("data", [])
            total_likes = sum(p.get("like_count", 0) for p in posts)
        else:
            print(f"Предупреждение при получении media ({media_resp.status_code}): {media_resp.text}")

        # 3. Охваты и показы через Insights (если доступно для аккаунта)
        reach = 0
        impressions = 0
        insights_resp = requests.get(
            f"{base_url}/insights",
            params={
                "metric": "reach,impressions",
                "period": "days_28",
                "access_token": INSTAGRAM_ACCESS_TOKEN,
            },
            timeout=15,
        )
        if insights_resp.status_code == 200:
            for item in insights_resp.json().get("data", []):
                name = item.get("name")
                values = item.get("values", [])
                val = values[-1].get("value", 0) if values else 0
                if name == "reach":
                    reach = val
                elif name == "impressions":
                    impressions = val

        return {
            "platform": "Instagram",
            "date": current_date,
            "followers": followers,
            "media_count": media_count,
            "reach": reach,
            "impressions": impressions,
            "likes": total_likes,
        }

    except requests.RequestException as e:
        print(f"Сетевая ошибка при запросе к Instagram: {e}")
        return _empty_metrics(current_date)