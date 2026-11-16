from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo


LOCAL_TIMEZONE = ZoneInfo("America/Sao_Paulo")


def to_local_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(LOCAL_TIMEZONE)


def format_local_date(value: datetime) -> str:
    return to_local_datetime(value).strftime("%d/%m/%Y")


def utc_month_bounds(month: date) -> tuple[datetime, datetime]:
    start_local = datetime.combine(month, time.min, tzinfo=LOCAL_TIMEZONE)
    if month.month == 12:
        next_month = date(month.year + 1, 1, 1)
    else:
        next_month = date(month.year, month.month + 1, 1)
    end_local = datetime.combine(next_month, time.min, tzinfo=LOCAL_TIMEZONE)

    return (
        start_local.astimezone(timezone.utc).replace(tzinfo=None),
        end_local.astimezone(timezone.utc).replace(tzinfo=None),
    )
