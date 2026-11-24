"""
Конфигурация проекта SMM-analytics scripts.

КАК ВСЁ НАСТРОИТЬ ДЛЯ РАБОТЫ:
1. Создайте файл `.env` в корне проекта (рядом с `main.py` и `README.md`) на основе `.env.example`.
   Файл `.env` должен быть добавлен в `.gitignore`, чтобы не выкладывать ключи на GitHub.
2. Установите зависимости в нужном окружении Python:
   `py -m pip install requests yt-dlp instaloader python-dotenv` (и остальные пакеты из `requirements.txt`).
3. Подготовьте Google Таблицу и сервисный аккаунт:
   - В Google Cloud Console создайте проект, включите Google Sheets API и создайте Service Account.
   - Скачайте JSON-ключ, переименуйте в `service_account.json` и положите в корень проекта.
   - Откройте `service_account.json`, скопируйте значение поля `client_email` и откройте доступ
     на редактирование этому email в вашей Google Таблице.
4. Заполните нужные поля в `.env` (пустые необязательные поля можно оставить пустыми).
5. При необходимости включите VPN / проверьте сеть, если парсинг отдельных площадок в вашем регионе
   требует обхода сетевых ограничений.
"""

import os
from dotenv import load_dotenv

load_dotenv()

#AI и Google Sheets

# API-ключ для генерации AI-выводов и аналитики (например, Groq Console или Google AI Studio).
# Где взять: в личном кабинете выбранного AI-провайдера в разделе API Keys.
AI_API_KEY = os.getenv("AI_API_KEY")

# ID целевой Google Таблицы, куда записываются отчёты.
# Где взять: из адресной строки таблицы вида:
# https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# Путь к JSON-файлу сервисного аккаунта Google Cloud.
# Где взять: Google Cloud Console -> IAM & Admin -> Service Accounts -> Keys -> Add Key -> JSON.
# Не забудьте выдать `client_email` из этого файла права "Редактор" на таблицу.
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "service_account.json")

#Instagram

# Имя пользователя (username) Instagram без символа `@`.
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")

# Числовой ID Instagram Business или Creator аккаунта для Graph API.
# Где взять: аккаунт должен быть привязан к странице Facebook; ID можно получить через
# Meta Graph API Explorer (/me/accounts -> instagram_business_account -> id).
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")

# Токен доступа Meta / Instagram Graph API (желательно long-lived токен).
# Где взять: Meta for Developers -> ваше приложение -> Graph API Explorer / Tools.
# Нужны разрешения на чтение профиля и инсайтов аккаунта/страницы.
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

#TikTok

# Имя пользователя (username) TikTok без символа `@`.
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")

# Опционально: ключ от RapidAPI, если используете сторонний API вместо локального `yt-dlp`.
# Где взять: rapidapi.com -> выбранный TikTok API -> вкладка Endpoints / Header `X-RapidAPI-Key`.
# Если оставить пустым, скрипт может работать через `yt-dlp` без ключа RapidAPI.
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Опционально: хост выбранного API на RapidAPI (заголовок `X-RapidAPI-Host`), например:
# `tiktok-scraper7.p.rapidapi.com`.
RAPIDAPI_TIKTOK_HOST = os.getenv("RAPIDAPI_TIKTOK_HOST")

# Опционально: полный URL эндпоинта на RapidAPI для получения статистики профиля/видео.
RAPIDAPI_TIKTOK_URL = os.getenv("RAPIDAPI_TIKTOK_URL")

#YouTube

# Полная ссылка на YouTube-канал, например: `https://www.youtube.com/@channel_name`.
YOUTUBE_CHANNEL_URL = os.getenv("YOUTUBE_CHANNEL_URL")