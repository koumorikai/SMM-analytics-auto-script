"""
Планировщик регулярного запуска сбора SMM-аналитики.

КАК НАСТРОИТЬ РАСПИСАНИЕ:
Библиотека `schedule` поддерживает интервалы в секундах/минутах/часах,
ежедневный запуск и запуск по конкретным дням недели. Метода `.every().month`
в ней нет — поэтому для ежемесячного отчёта проверяем нужный день месяца
внутри функции-обёртки (`run_monthly_if_needed`).

Примеры настройки расписания:
1. Каждый день в 09:00:
   schedule.every().day.at("09:00").do(run_pipeline)

2. Раз в N дней (например, каждые 7 дней в 10:00):
   schedule.every(7).days.at("10:00").do(run_pipeline)

3. В конкретный день недели (например, каждый понедельник в 09:00):
   schedule.every().monday.at("09:00").do(run_pipeline)

4. Раз в месяц в заданное число (по умолчанию 1-е число месяца в 09:00):
   Задаётся через переменную `SCHEDULE_DAY_OF_MONTH` в `.env` (например, `1` или `15`)
   и время `SCHEDULE_TIME` (например, `09:00`). Скрипт проверяет каждую минуту
   в 09:00, совпало ли текущее число месяца с нужным.

КАК ЗАПУСКАТЬ:
- В открытом окне терминала (пока работает — скрипт ждёт триггера):
  `py schedule/scheduler.py` (из корня проекта `D:\\projects\\scripts\\SMM-analytics scripts`).
- Для запуска по расписанию без постоянно открытого окна VS Code лучше использовать
  Планировщик заданий Windows (Task Scheduler) с разовым вызовом `main.py`.
"""

import os
import time
from datetime import datetime
import schedule
from main import run_pipeline


def _get_target_day_of_month() -> int:
    """Читает целевое число месяца (1..28) из окружения, по умолчанию 1."""
    raw = os.getenv("SCHEDULE_DAY_OF_MONTH", "1").strip()
    try:
        day = int(raw)
        return max(1, min(28, day))
    except ValueError:
        return 1


def _run_monthly_job(target_day: int) -> None:
    """Запускает пайплайн только в указанный день месяца."""
    today = datetime.now().day
    if today == target_day:
        run_pipeline()
    else:
        print(f"Сегодня {today}-е число; запуск запланирован на {target_day}-е число.")


def start_scheduler() -> None:
    """Запускает фоновый планировщик для регулярного выполнения отчётов."""
    mode = os.getenv("SCHEDULE_MODE", "monthly").strip().lower()
    run_time = os.getenv("SCHEDULE_TIME", "09:00").strip()
    target_day = _get_target_day_of_month()

    if mode == "daily":
        schedule.every().day.at(run_time).do(run_pipeline)
        print(f"Планировщик запущен: ежедневно в {run_time}.")
    elif mode == "weekly":
        weekday = os.getenv("SCHEDULE_WEEKDAY", "monday").strip().lower()
        day_job = getattr(schedule.every(), weekday, schedule.every().monday)
        day_job.at(run_time).do(run_pipeline)
        print(f"Планировщик запущен: каждый {weekday} в {run_time}.")
    else:
        # Ежедневная проверка в заданное время срабатывает только в нужный день месяца
        schedule.every().day.at(run_time).do(_run_monthly_job, target_day=target_day)
        print(f"Планировщик запущен: ежемесячно {target_day}-го числа в {run_time}.")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start_scheduler()