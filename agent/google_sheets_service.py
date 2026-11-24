import gspread
from conf.config import GOOGLE_SERVICE_ACCOUNT_FILE, SPREADSHEET_ID

def save_report_to_sheet(metrics: dict, insights: str, platform: str = "Instagram"):
    """
    Сохраняет метрики и AI-аналитику на отдельную вкладку конкретной платформы
    (Instagram, YouTube, TikTok) в Google Таблице.
    """
    try:
        # Авторизация по сервисному аккаунту
        gc = gspread.service_account(filename=GOOGLE_SERVICE_ACCOUNT_FILE)
        
        # Открытие таблицы по ID
        spreadsheet = gc.open_by_key(SPREADSHEET_ID)
        
        # Выбор или создание отдельной вкладки под каждую соцсеть
        try:
            sheet = spreadsheet.worksheet(platform)
        except gspread.exceptions.WorksheetNotFound:
            # еще нет, создаем его и добавляем шапку таблицы
            sheet = spreadsheet.add_worksheet(title=platform, rows=100, cols=10)
            sheet.append_row(["Date", "Followers Growth", "Reach", "Impressions", "Likes", "AI Insights"])
        
        # Подготовка строки с данными
        row = [
            metrics.get("date", "N/A"),
            metrics.get("followers_growth", 0),
            metrics.get("reach", 0),
            metrics.get("impressions", 0),
            metrics.get("likes", 0),
            insights
        ]
        
        # Добавление строки на нужный лист
        sheet.append_row(row)
        print(f"Данные успешно записаны на вкладку [{platform}] в Google Таблицу!")
        
    except Exception as e:
        print(f"Ошибка при записи в Google Таблицу ({platform}): {e}")