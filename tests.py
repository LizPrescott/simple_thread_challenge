import constants
from script import calculate_reimbursement

"""
We can assume for now that all input will be in this consistent format
and that projects in each set will be chronological
"""

set_1 = ["Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15"]

set_2 = [
    "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
    "Project 2: High Cost City Start Date: 9/2/15 End Date: 9/6/15",
    "Project 3: Low Cost City Start Date: 9/6/15 End Date: 9/8/15"
  ]

set_3 = [
  "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15",
  "Project 2: High Cost City Start Date: 9/5/15 End Date: 9/7/15",
  "Project 3: High Cost City Start Date: 9/8/15 End Date: 9/8/15",
]
set_4 = [
  "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
  "Project 2: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
  "Project 3: High Cost City Start Date: 9/2/15 End Date: 9/2/15",
  "Project 4: High Cost City Start Date: 9/2/15 End Date: 9/3/15"
]


def test_base_case():
    assert calculate_reimbursement(set_1) == [
        {"Project 1": (constants.TRAVEL_DAY_LOW * 2) + constants.FULL_DAY_LOW}
    ]


def test_high_to_low_overlap():
    assert calculate_reimbursement(set_2) == [
      {"Project 1": constants.TRAVEL_DAY_LOW},
      # Assume higher cost full day should be reimbursed
      {"Project 2": constants.FULL_DAY_HIGH*5},
      # Don't count the first full day since, already reimbursed in project 2
      {"Project 3": constants.TRAVEL_DAY_LOW + constants.FULL_DAY_LOW}
    ]


def test_multiple_projects_no_overlaps():
    assert calculate_reimbursement(set_3) == [
      {"Project 1": constants.TRAVEL_DAY_LOW*2 + constants.FULL_DAY_LOW},
      {"Project 2": constants.TRAVEL_DAY_HIGH + (constants.FULL_DAY_HIGH*2)},
      {"Project 3": constants.TRAVEL_DAY_HIGH}
    ]


def test_travel_day_perfect_overlap():
    assert calculate_reimbursement(set_4) == [
      # Assum when one of the overlap days is a travel day, both are
      {"Project 1": constants.TRAVEL_DAY_LOW},
      {"Project 2": 0.0},
      {"Project 3": constants.FULL_DAY_HIGH},
      # Do not count the full day, which was reimbursed in Project 3
      {"Project 4": constants.TRAVEL_DAY_HIGH}
    ]
