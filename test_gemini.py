import requests
import json
from conf.config import GEMINI_API_KEY

# URL для прямого обращения 
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"

headers = {
    'Content-Type': 'application/json'
}

data = {
    "contents": [{
        "parts": [{"text": "Привет! Ответь коротко: ты на связи?"}]
    }]
}

print("Отправка прямого HTTP-запроса к Gemini API...")

try:
    # Устанавливаем таймоут
    response = requests.post(url, headers=headers, json=data, timeout=15)
    
    print(f"Статус код ответа: {response.status_code}")
    print("Ответ сервера:", response.text)
    
    if response.status_code == 200:
        print(" Успех! Соединение с Gemini работает.")
    else:
        print(" Ошибка от сервера Google. Проверьте правильность API-ключа.")
        
except requests.exceptions.Timeout:
    print(" Ошибка: Время ожидания истекло (Timeout). Скрипт не смог доступиться до серверов Google.")
    print(" Совет: Попробуйте включить VPN или проверить интернет-соединение.")
except Exception as e:
    print(f" Произошла ошибка сети: {e}")