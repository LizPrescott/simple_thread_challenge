import pytest
from app.constants import (
  FULL_DAY_HIGH,
  FULL_DAY_LOW,
  TRAVEL_DAY_HIGH,
  TRAVEL_DAY_LOW
)
from app.script import Reimbursement

"""
We can assume for now that all input will be in this consistent format
and that projects in each set will be chronological
"""


def test_empty():
    assert Reimbursement([]).calculate() == 0


def test_base_case():
    input = ["Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15"]
    project_1_total = (TRAVEL_DAY_LOW * 2) + FULL_DAY_LOW
    reimbursement_total = Reimbursement(input).calculate()

    assert reimbursement_total  == project_1_total
    print(f"Scenario 1 Total: {project_1_total}")


def test_no_overlap():
    input = [
      "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
      "Project 2: Low Cost City Start Date: 9/6/15 End Date: 9/8/15"
    ]
    project_1_total = TRAVEL_DAY_LOW
    project_2_total = TRAVEL_DAY_LOW*2 + FULL_DAY_LOW
    assert Reimbursement(input).calculate() == sum([
         project_1_total, project_2_total
         ])


def test_high_to_low_overlap():
    input = [
      "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
      "Project 2: High Cost City Start Date: 9/2/15 End Date: 9/6/15",
      "Project 3: Low Cost City Start Date: 9/6/15 End Date: 9/8/15"
    ]
    project_1_total = TRAVEL_DAY_LOW
    project_2_total = FULL_DAY_HIGH*5  # 9/2 + 9/3 + 9/4 + 9/5 + 9/6
    project_3_total = TRAVEL_DAY_LOW + FULL_DAY_LOW  # 9/7 + 9/8
    reimbursement_total = Reimbursement(input).calculate()

    assert reimbursement_total  == sum([
         project_1_total, project_2_total, project_3_total
         ])
    print(f"Scenario 2 Total: {reimbursement_total}")


def test_contiguous_projects():
    input = [
      "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15",
      "Project 2: High Cost City Start Date: 9/5/15 End Date: 9/7/15",
      "Project 3: High Cost City Start Date: 9/8/15 End Date: 9/8/15",
    ]
    project_1_total = ((TRAVEL_DAY_LOW*2) + FULL_DAY_LOW)
    project_2_total = (TRAVEL_DAY_HIGH + (FULL_DAY_HIGH*2))
    project_3_total = TRAVEL_DAY_HIGH
    reimbursement_total = Reimbursement(input).calculate()

    assert reimbursement_total  == sum([
      project_1_total, project_2_total, project_3_total
    ])
    print(f"Scenario 3 Total: {reimbursement_total}")


# Covers opening pair where opening project is low cost
@pytest.mark.parametrize('project_2_cost, project_2_result', [
    ('Low', TRAVEL_DAY_LOW), ('High', TRAVEL_DAY_HIGH)
    ])
def test_travel_day_perfect_overlap(project_2_cost, project_2_result):
    input = [
      "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
      f"Project 2: {project_2_cost} Cost City Start Date: 9/1/15 End Date: 9/1/15",
      "Project 3: High Cost City Start Date: 9/2/15 End Date: 9/2/15",
      "Project 4: High Cost City Start Date: 9/2/15 End Date: 9/3/15"
    ]
    project_1_total = 0
    project_2_total = project_2_result
    project_3_total = FULL_DAY_HIGH
    project_4_total = TRAVEL_DAY_HIGH
    reimbursement_total = Reimbursement(input).calculate()

    assert reimbursement_total  == sum([
      project_1_total, project_2_total, project_3_total, project_4_total
    ])
    if (project_2_result == TRAVEL_DAY_LOW):
      print(f"Scenario 4 Total: {reimbursement_total}")


# Covers opening pair overlap with high cost
@pytest.mark.parametrize('project_2_cost', ['High', 'Low'])
def test_travel_day_multi_overlap(project_2_cost):
    input = [
      "Project 1: High Cost City Start Date: 9/1/15 End Date: 9/2/15",
      f"Project 2: {project_2_cost} Cost City Start Date: 9/1/15 End Date: 9/2/15",
      "Project 3: High Cost City Start Date: 9/3/15 End Date: 9/3/15",
      "Project 4: High Cost City Start Date: 9/3/15 End Date: 9/4/15"
    ]
    project_1_total = TRAVEL_DAY_HIGH + FULL_DAY_HIGH
    project_2_total = 0
    project_3_total = FULL_DAY_HIGH
    project_4_total = TRAVEL_DAY_HIGH
    assert Reimbursement(input).calculate() == sum([
      project_1_total, project_2_total, project_3_total, project_4_total
    ])
  

@pytest.mark.parametrize('project_2_cost, project_2_result', [
    ('Low', TRAVEL_DAY_LOW*2 + FULL_DAY_LOW*2),
    ('High', TRAVEL_DAY_HIGH*2 + FULL_DAY_HIGH*2)
    ])
def test_short_opener(project_2_cost, project_2_result):
    input = [
        "Project 1: Low Cost City Start Date: 3/15/15 End Date: 3/15/15",
        f"Project 2: {project_2_cost} Cost City Start Date: 3/15/15 End Date: 3/18/15",
        "Project 3: High Cost City Start Date: 4/1/15 End Date: 4/3/15"
    ]
    project_1_total = 0
    project_2_total = project_2_result
    project_3_total = TRAVEL_DAY_HIGH*2 + FULL_DAY_HIGH
    assert Reimbursement(input).calculate() == sum([
        project_1_total, project_2_total, project_3_total
    ])


@pytest.mark.parametrize('project_2_cost, project_2_result', [
    ('Low', TRAVEL_DAY_LOW + FULL_DAY_LOW*2),
    ('High', TRAVEL_DAY_HIGH + FULL_DAY_HIGH*2)
    ])
def test_high_cost_short_opener(project_2_cost, project_2_result):
    input = [
        "Project 1: High Cost City Start Date: 3/15/15 End Date: 3/15/15",
        f"Project 2: {project_2_cost} Cost City Start Date: 3/15/15 End Date: 3/18/15",
        "Project 3: High Cost City Start Date: 4/1/15 End Date: 4/3/15"
    ]
    project_1_total = TRAVEL_DAY_HIGH
    project_2_total = project_2_result
    project_3_total = TRAVEL_DAY_HIGH*2 + FULL_DAY_HIGH
    assert Reimbursement(input).calculate() == sum([
        project_1_total, project_2_total, project_3_total
    ])


@pytest.mark.parametrize('project_3_cost', ['High', 'Low'])
def test_mid_set_overlap(project_3_cost):
    input = [
         "Project 1: Low Cost City Start Date: 1/1/15 End Date: 1/1/15",
         "Project 2: High Cost City Start Date: 3/25/15 End Date: 3/28/15",
         f"Project 3: {project_3_cost} Cost City Start Date: 3/25/15 End Date: 3/28/15"
    ]
    assert Reimbursement(input).calculate() == sum([
        TRAVEL_DAY_LOW,
        (TRAVEL_DAY_HIGH*2)+(FULL_DAY_HIGH*2)
    ])

