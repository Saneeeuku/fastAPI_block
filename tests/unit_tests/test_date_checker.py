from datetime import date, timedelta

from pytest import mark, raises as pyraises

from src.repos.utils_repo import date_check
from src.schemas.bookings_schemas import _convert_str_to_date
from src.exceptions import DateViolationException


@mark.parametrize(
    "date_from, date_to, resp",
    [
        ("2026-12-01", "2026-11-01", DateViolationException),
        ("2023-12-01", "2024-11-01", DateViolationException),
        ("2026-12-01", "2023-12-01", DateViolationException),
    ],
)
def test_date_checks(date_from, date_to, resp):
    today = date.today()
    date_from = _convert_str_to_date(date_from)
    date_to = _convert_str_to_date(date_to)

    assert date_check(today, today + timedelta(days=1)) is None

    with pyraises(DateViolationException):
        date_check(today, today)

    with pyraises(DateViolationException):
        date_check(date_from, date_to)
