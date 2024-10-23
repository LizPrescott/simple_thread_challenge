from app.constants import (
  FULL_DAY_HIGH,
  FULL_DAY_LOW,
  TRAVEL_DAY_HIGH,
  TRAVEL_DAY_LOW
)
from app.script import calculate_reimbursement

"""
We can assume for now that all input will be in this consistent format
and that projects in each set will be chronological
"""


def test_base_case():
    input = ["Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15"]
    project_1_total = (TRAVEL_DAY_LOW * 2) + FULL_DAY_LOW
    assert calculate_reimbursement(input) == project_1_total
    # assert calculate_total(input) == project_1_total


def test_no_overlap():
    input = [
      "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
      "Project 2: Low Cost City Start Date: 9/6/15 End Date: 9/8/15"
    ]
    project_1_total = TRAVEL_DAY_LOW
    project_2_total = TRAVEL_DAY_LOW*2 + FULL_DAY_LOW
    assert calculate_reimbursement(input) == sum([
         project_1_total, project_2_total
         ])


def test_high_to_low_overlap():
    input = [
      "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
      "Project 2: High Cost City Start Date: 9/2/15 End Date: 9/6/15",
      "Project 3: Low Cost City Start Date: 9/6/15 End Date: 9/8/15"
    ]
    project_1_total = TRAVEL_DAY_LOW
    project_2_total = FULL_DAY_HIGH*5 # 9/2 + 9/3 + 9/4 + 9/5 + 9/6
    project_3_total = TRAVEL_DAY_LOW + FULL_DAY_LOW # 9/7 + 9/8
    assert calculate_reimbursement(input) == sum([
         project_1_total, project_2_total, project_3_total
         ])
    # assert calculate_total(input) == sum([
    #      project_1_total, project_2_total, project_3_total
    #      ])


def test_contiguous_projects():
    input = [
      "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15",
      "Project 2: High Cost City Start Date: 9/5/15 End Date: 9/7/15",
      "Project 3: High Cost City Start Date: 9/8/15 End Date: 9/8/15",
    ]
    project_1_total = ((TRAVEL_DAY_LOW*2) + FULL_DAY_LOW)
    project_2_total = (TRAVEL_DAY_HIGH + (FULL_DAY_HIGH*2))
    project_3_total = TRAVEL_DAY_HIGH
    assert calculate_reimbursement(input) == sum([ # sum([165, 225, 55])
      project_1_total, project_2_total, project_3_total
    ])
    # assert calculate_total(input) == sum([
    #   project_1_total, project_2_total, project_3_total
    # ])


def test_travel_day_perfect_overlap():
    input = [
      "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
      "Project 2: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
      "Project 3: High Cost City Start Date: 9/2/15 End Date: 9/2/15",
      "Project 4: High Cost City Start Date: 9/2/15 End Date: 9/3/15"
    ]
    project_1_total = 0
    project_2_total = TRAVEL_DAY_LOW
    project_3_total = FULL_DAY_HIGH
    project_4_total = TRAVEL_DAY_HIGH
    # assert calculate_total(input) == sum([
    #   project_1_total, project_2_total, project_3_total, project_4_total
    # ])
    assert calculate_reimbursement(input) == sum([
      project_1_total, project_2_total, project_3_total, project_4_total
    ])
    
