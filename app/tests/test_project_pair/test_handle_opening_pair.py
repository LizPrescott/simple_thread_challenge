import pytest

from datetime import date
from app.script import Project, ProjectPair


@pytest.mark.parametrize('project_b_high_cost', [True, False])
def test_low_cost_first(project_b_high_cost):
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

    pair.handle_opening_pair()
    assert project_a.full_days == 1
    assert project_a.travel_days == 1
    assert project_b.full_days == 2
    assert project_b.travel_days == 1

@pytest.mark.parametrize('project_b_high_cost', [True, False])
def test_high_cost_first(project_b_high_cost):
    project_a = Project(
        name="Project a",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 28),
        is_high_cost=True
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

    pair.handle_opening_pair()
    assert project_a.full_days == 3
    assert project_a.travel_days == 1
    assert project_b.full_days == 0
    assert project_b.travel_days == 1

@pytest.mark.parametrize('project_a_high_cost', [True, False])
@pytest.mark.parametrize('project_b_high_cost', [True, False])
def test_contiguous(project_a_high_cost, project_b_high_cost):
    project_a = Project(
        name="Project a",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 28),
        is_high_cost=project_a_high_cost
        )
    assert project_a.travel_days == 2
    assert project_a.full_days == 2

    project_b = Project(
        name="Project b",
        start_date=date(2015, 3, 29),
        end_date=date(2015, 3, 31),
        is_high_cost=project_b_high_cost
        )
    assert project_b.full_days == 1
    assert project_b.travel_days == 2
    
    pair = ProjectPair(project_a, project_b)
    assert pair.overlap == 0

    pair.handle_opening_pair()
    assert project_a.full_days == 3
    assert project_a.travel_days == 1
    assert project_b.full_days == 2
    assert project_b.travel_days == 1

@pytest.mark.parametrize('project_b_high_cost', [True, False])
def test_short_opener(project_b_high_cost):
    project_a = Project(
        name="Project a",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 25),
        is_high_cost=False
        )
    assert project_a.travel_days == 1
    assert project_a.full_days == 0

    project_b = Project(
        name="Project b",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 28),
        is_high_cost=project_b_high_cost
        )
    assert project_b.full_days == 2
    assert project_b.travel_days == 2
    
    pair = ProjectPair(project_a, project_b)
    assert pair.overlap == 1

    pair.handle_opening_pair()
    assert project_a.full_days == 0
    assert project_a.travel_days == 0
    assert project_b.full_days == 2
    assert project_b.travel_days == 2

@pytest.mark.parametrize('project_b_high_cost', [True, False])
def test_short_high_cost_opener(project_b_high_cost):
    project_a = Project(
        name="Project a",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 25),
        is_high_cost=True
        )
    assert project_a.travel_days == 1
    assert project_a.full_days == 0

    project_b = Project(
        name="Project b",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 28),
        is_high_cost=False
        )
    assert project_b.full_days == 2
    assert project_b.travel_days == 2
    
    pair = ProjectPair(project_a, project_b)
    assert pair.overlap == 1

    pair.handle_opening_pair()
    assert project_a.full_days == 0
    assert project_a.travel_days == 1
    assert project_b.full_days == 2
    assert project_b.travel_days == 1


@pytest.mark.parametrize('project_b_high_cost', [True, False])
def test_perfect_overlap_low(project_b_high_cost):
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
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 28),
        is_high_cost=project_b_high_cost
        )
    assert project_b.full_days == 2
    assert project_b.travel_days == 2
    
    pair = ProjectPair(project_a, project_b)
    assert pair.overlap == 4

    pair.resolve()
    assert project_a.full_days == 0
    assert project_a.travel_days == 0
    assert project_b.full_days == 2
    assert project_b.travel_days == 2

@pytest.mark.parametrize('project_b_high_cost', [True, False])
def test_perfect_overlap(project_b_high_cost):
    project_a = Project(
        name="Project a",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 28),
        is_high_cost=True
        )
    assert project_a.travel_days == 2
    assert project_a.full_days == 2

    project_b = Project(
        name="Project b",
        start_date=date(2015, 3, 25),
        end_date=date(2015, 3, 28),
        is_high_cost=project_b_high_cost
        )
    assert project_b.full_days == 2
    assert project_b.travel_days == 2
    
    pair = ProjectPair(project_a, project_b)
    assert pair.overlap == 4

    pair.handle_opening_pair()
    assert project_a.full_days == 2
    assert project_a.travel_days == 2
    assert project_b.full_days == 0
    assert project_b.travel_days == 0