from datetime import date

def get_week_from_date(d:date) -> tuple[int, int]:
    iso_calendar = d.isocalendar()
    return iso_calendar[1], iso_calendar[0]

