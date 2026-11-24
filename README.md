# SMM-analytics scripts

Скрипты для сбора статистики по соцсетям (**Instagram**, **TikTok**, **YouTube**), формирования AI-выводов и выгрузки отчётов в **Google Таблицы**.

---


## 1. За что отвечает каждый файл и папка

```text
SMM-analytics scripts/
├── main.py                     # Главная точка входа: запускает сбор метрик, AI-анализ и запись в таблицу
├── conf/
│   └── config.py               # Загружает переменные из .env и хранит настройки/инструкцию по ключам
├── handlers/
│   ├── instagram_service.py    # Получение метрик Instagram (через Graph API / инсайты / публикации)
│   ├── tiktok_service.py       # Получение метрик TikTok (через RapidAPI или yt-dlp)
│   └── youtube_service.py      # Получение метрик YouTube-канала и видео
├── agent/
│   ├── ai_service.py           # Генерация аналитических выводов и рекомендаций с помощью AI API
│   └── google_sheets_service.py# Подключение к Google Sheets API и запись строк отчёта в таблицу
├── schedule/
│   └── scheduler.py            # Фоновый планировщик регулярного запуска пайплайна по расписанию
├── service_account.json        # Ключ сервисного аккаунта Google Cloud (НЕ добавлять в Git!)
├── .env                        # Локальные ключи API, ID таблицы и аккаунты (НЕ добавлять в Git!)
├── .env.example                # Шаблон файла .env для других пользователей
├── .gitignore                  # Список файлов и папок, которые Git должен игнорировать
├── requirements.txt            # Список необходимых Python-библиотек
└── gemeni.md                   # Контекст и правила работы проекта для AI-ассистента
```
all requirements -->
```powershell

 py -m pip install requests python-dotenv yt-dlp instaloader schedule google-api-python-client google-auth 
