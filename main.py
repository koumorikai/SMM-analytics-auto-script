"""
Точка входа для запуска пайплайна сбора SMM-аналитики (Instagram, TikTok, YouTube),
генерации AI-выводов и выгрузки отчётов в Google Таблицы.

ПЕРЕД ЗАПУСКОМ:
- Все ключи API, ID таблицы и аккаунты задаются через файл `.env` и считываются в `conf/config.py`.
- Загляните в `conf/config.py` — там расписано, где взять каждый ключ, как настроить
  `service_account.json` и выдать доступ к Google Таблице.
- Не забудьте убедиться, что `.env` и `service_account.json` добавлены в `.gitignore`
  и не попадают в репозиторий.
"""




from handlers.instagram_service import fetch_instagram_metrics
from handlers.youtube_service import fetch_youtube_metrics
from handlers.tiktok_service import fetch_tiktok_metrics

from agent.ai_service import generate_report_insights
from agent.google_sheets_service import save_report_to_sheet

def run_full_pipeline():
    
    platforms = [
        ("Instagram", fetch_instagram_metrics),
        ("YouTube", fetch_youtube_metrics),
        ("TikTok", fetch_tiktok_metrics)
    ]
    
    for platform_name, fetch_func in platforms:
        print(main_step_header(platform_name))
        
        # Сбор метрик
        metrics = fetch_func()
        

        insights = generate_report_insights(metrics, platform=platform_name)
        

        save_report_to_sheet(metrics, insights, platform=platform_name)
        print("-" * 50)

    print("Все отчеты успешно сформированы и выгружены!")

def main_step_header(platform):
    return f"\nОбработка платформы: {platform}"

if __name__ == "__main__":
    run_full_pipeline()