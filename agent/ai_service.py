from openai import OpenAI
from conf.config import GROQ_API_KEY

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

def generate_report_insights(metrics: dict, platform: str = "Instagram") -> str:
    """Генерирует глубокую SMM-аналитику и бизнес-рекомендации с помощью Groq."""
    prompt = f"""
    Ты экспертный SMM-аналитик и маркетолог. Проведи глубокий анализ ежемесячного отчета по платформе {platform}:
    - Прирост подписчиков: {metrics.get('followers_growth', 0)}
    - Охваты (Reach): {metrics.get('reach', 0)}
    - Просмотры (Impressions): {metrics.get('impressions', 0)}
    - Лайки: {metrics.get('likes', 0)}
    
    Дай структурированный ответ:
    1. Главный вывод по динамике ключевых показателей.
    2. Оценка вовлеченности аудитории.
    3. 1 конкретная стратегическая рекомендация для роста на следующий месяц.
    """
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка генерации аналитики ИИ: {e}"