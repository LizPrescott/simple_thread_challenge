import pytest

from datetime import date
from app.script import Project, ProjectPair

@pytest.mark.parametrize('project_b_high_cost', [True, False])
def test_low_cost_overlap(project_b_high_cost):
    project_a = Project(
        name="Project a",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 28),
        is_high_cost=False
        )
    assert project_a.travel_days == 2
    assert project_a.full_days == 2

    project_b = Project(
        name="Project b",
        start_date=date(2015, 3, 27),
        end_date=date(2015, 3, 29),
        is_high_cost=project_b_high_cost
        )
    assert project_b.full_days == 1
    assert project_b.travel_days == 2
    
    pair = ProjectPair(project_a, project_b)
    assert pair.overlap == 2

    pair.handle_overlap()
    assert project_a.full_days == 1
    assert project_a.travel_days == 1
    assert project_b.full_days == 2
    assert project_b.travel_days == 1


def test_opening_pair():
    project_a = Project(
        name="Project a",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 28),
        is_high_cost=False
        )
    assert project_a.travel_days == 2
    assert project_a.full_days == 2

    project_b = Project(
        name="Project b",
        start_date=date(2015, 3, 27),
        end_date=date(2015, 3, 29),
        is_high_cost=False
        )
    assert project_b.full_days == 1
    assert project_b.travel_days == 2
    
    pair = ProjectPair(project_a, project_b)
    assert pair.overlap == 2

    pair.handle_opening_pair()
    assert project_a.full_days == 1
    assert project_a.travel_days == 1
    assert project_b.full_days == 2
    assert project_b.travel_days == 1