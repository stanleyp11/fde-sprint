from datetime import date

import pytest

from proration import prorate


def test_full_period_on_first_day():
    assert prorate(300.0, date(2026, 10, 1), date(2026, 10, 31), date(2026, 10, 1)) == 300.0


def test_half_period():
    # 30-day period, 15 days left
    assert prorate(300.0, date(2026, 10, 1), date(2026, 10, 31), date(2026, 10, 16)) == 150.0


def test_annual_upgrade():
    # 365-day year, upgrade with 100 days left
    assert prorate(1200.0, date(2026, 1, 1), date(2027, 1, 1), date(2026, 9, 23)) == 328.77


def test_change_outside_period_is_rejected():
    with pytest.raises(ValueError):
        prorate(300.0, date(2026, 10, 1), date(2026, 10, 31), date(2026, 10, 31))
    with pytest.raises(ValueError):
        prorate(300.0, date(2026, 10, 1), date(2026, 10, 31), date(2026, 9, 30))
