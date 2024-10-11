from .. import constants

"""
We can assume for now that all input will be in this consistent format
and that projects in each set will be chronological
"""

set_1 =
  ["Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15"]

set_2 =
  [
    "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
  "Project 2: High Cost City Start Date: 9/2/15 End Date: 9/6/15",
  "Project 3: Low Cost City Start Date: 9/6/15 End Date: 9/8/15"
  ]

set_3 = 
[
  "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15",
  "Project 2: High Cost City Start Date: 9/5/15 End Date: 9/7/15",
  "Project 3: High Cost City Start Date: 9/8/15 End Date: 9/8/15",
]
set_4 = 
[
  "Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
  "Project 2: Low Cost City Start Date: 9/1/15 End Date: 9/1/15",
  "Project 3: High Cost City Start Date: 9/2/15 End Date: 9/2/15",
  "Project 4: High Cost City Start Date: 9/2/15 End Date: 9/3/15
]

assert calculate_reimbursement(set_1) == [{"Project 1": }]