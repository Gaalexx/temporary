import calendar, math
from datetime import datetime, date, timedelta
from typing import Tuple, Iterable


class GregorianCalendar:
    MONTH_NAMES = [
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь",
    ]

    @staticmethod
    def setfirstweekday(weekday: int) -> None:
        calendar.setfirstweekday(weekday)

    @staticmethod
    def current_date() -> Tuple[int, int, int]:
        today_date = datetime.date(datetime.now())
        return today_date.day, today_date.month, today_date.year

    @staticmethod
    def month_days(year: int, month: int) -> Iterable[date]:
        return calendar.Calendar(calendar.firstweekday()).itermonthdates(year, month)

    def prev_month_and_year(year: int, month: int) -> Tuple[int, int]:
        previous_month_date = date(year, month, 1) - timedelta(days=2)
        return previous_month_date.month, previous_month_date.year

    @staticmethod
    def monthrange(year: int, month: int) -> Tuple[int, int]:
        return calendar.monthrange(year, month)

    @staticmethod
    def next_month_and_year(year: int, month: int) -> Tuple[int, int]:
        last_day_of_month = calendar.monthrange(year, month)[1]
        next_month_date = date(year, month, last_day_of_month) + timedelta(days=2)
        return next_month_date.month, next_month_date.year

    @staticmethod
    def count_weeks(year: int, month: int) -> int:
        return len(calendar.Calendar(calendar.firstweekday()).monthdatescalendar(year, month))

    @staticmethod
    def num_weekday(year: int, month: int, day: int) -> int:
        return calendar.weekday(year, month, day)

    @staticmethod
    def num_weekdays(year: int, month: int, day: int) -> int:
        return GregorianCalendar.num_weekday(year, month, day)

    @staticmethod
    def num_week_in_month_by_date(year: int, month: int, day: int) -> int:
        # Определяем номер дня недели на первое число текущего месяца
        num_week_first_day_current_month = GregorianCalendar.num_weekday(year, month, 1)

        # Определяем номер недели в месяце по дате
        num_week_in_month_by_date = math.ceil((num_week_first_day_current_month + day) / 7) - 1

        return num_week_in_month_by_date

    @staticmethod
    def week_days(year, month, week) -> Iterable[date]:
        return calendar.Calendar(calendar.firstweekday()).monthdatescalendar(year, month)[week]

