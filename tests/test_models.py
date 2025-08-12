from datetime import date

import pytest

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from project_registry.models import Project


def test_project_requires_end_or_duration():
    with pytest.raises(ValueError):
        Project(start_date=date(2023, 1, 1))
    with pytest.raises(ValueError):
        Project(start_date=date(2023, 1, 1), end_date=date(2023, 6, 1), duration_months=6)
    p = Project(start_date=date(2023, 1, 1), end_date=date(2023, 6, 1))
    assert p.end_date == date(2023, 6, 1)
    p2 = Project(start_date=date(2023, 1, 1), duration_months=12)
    assert p2.duration_months == 12
