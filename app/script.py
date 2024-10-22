
from datetime import date
from app.constants import (
    FULL_DAY_HIGH,
    FULL_DAY_LOW,
    TRAVEL_DAY_HIGH,
    TRAVEL_DAY_LOW
)


class Reimbursement:
    """
    A generator class, for looping over all projects in a set
    """
    def __init__(self, list_of_strings):
        self.projects = [Project.from_string(x) for x in list_of_strings]

    def __iter__(self):
        for project in self.projects:
            yield project


class Project:
    def __init__(self, name, start_date, end_date, is_high_cost):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.is_high_cost = is_high_cost
        self.travel_days = 2
        # Allow full days to get below zero to account for diffs in travel days
        self.full_days = (self.end_date - self.start_date).days - 1
        self.duration = max(((self.end_date - self.start_date).days - 1),0)

    @staticmethod
    def parse_date(date_string):
        month, day, year = date_string.strip().split("/")
        year = ("20" + year).split(" ")[0]
        return date(int(year), int(month), int(day))

    @classmethod
    def from_string(cls, string):
        name, cost_string, start_date_str, end_date_str = string.split(":")
        end_date = cls.parse_date(end_date_str)
        start_date = cls.parse_date(start_date_str)
        is_high_cost = "High" in cost_string
        return cls(name, start_date, end_date, is_high_cost)

    def remove_travel_day(self):
        self.travel_days -= 1
        self.full_days += 1

    def calculate_project_cost(self):
        if self.is_high_cost:
            travel_day_cost = TRAVEL_DAY_HIGH
            full_day_cost = FULL_DAY_HIGH
        else:
            travel_day_cost = TRAVEL_DAY_LOW
            full_day_cost = FULL_DAY_LOW
        return max((self.full_days * full_day_cost) + (travel_day_cost * self.travel_days), 0)

    def project_overlap(self, next_project):
        return next_project.start_date.day - self.end_date.day + 1


def calculate_reimbursement(list_of_strings):
    # Handles empty project sets
    if not list_of_strings:
        return
    starting_iter = iter(Reimbursement(list_of_strings))
    current_project = next(starting_iter)
    # Single project is a special case
    if len(list_of_strings) == 1:
        return current_project.calculate_project_cost()
    total = 0.0
    for next_project in starting_iter:
        project_overlap = current_project.project_overlap(next_project)
        if project_overlap:
            pass
        if (next_project.start_date - current_project.end_date).days == 1:
            current_project.remove_travel_day()
            next_project.remove_travel_day()
        elif current_project.end_date >= next_project.start_date:
            current_project.remove_travel_day()
            next_project.remove_travel_day()
            if not next_project.is_high_cost:
                next_project.full_days -= project_overlap
            else:
                current_project.full_days -= project_overlap
        total += current_project.calculate_project_cost()
        current_project = next_project
    # Final Project costs
    total += current_project.calculate_project_cost()
    return total

# Experimental refactor that I'm not read to let go yet
# 
# def calculate_total(list_of_strings):
#     pass
#     # Handles empty project sets
#     if not list_of_strings:
#         return 0.0
#     proj_iter = iter(Reimbursement(list_of_strings))
#     proj_a = next(proj_iter)
#     total = 0.0
#     high_cost = proj_a.is_high_cost
#     travel_cost = TRAVEL_DAY_HIGH if high_cost else TRAVEL_DAY_LOW
#     full_cost = FULL_DAY_HIGH if high_cost else FULL_DAY_LOW
#     for proj_b in proj_iter:
#         pass
#         total += travel_cost * 2
#         total += full_cost * current_project.duration
#         proj_a = proj_b
#     total += travel_cost
#     return total
    # Find the first travel day
    # Many projects can start on the same day and be a single day
    # while current_project.start_date == current_project.end_date == next_project.start_date:
    #     current_project = next(proj_iter)
    #     next_project = next(next_proj_iter)
    #     high_cost = high_cost or current_project.is_high_cost
    # travel_cost = TRAVEL_DAY_HIGH if high_cost else TRAVEL_DAY_LOW
    # full_cost = FULL_DAY_HIGH if high_cost else FULL_DAY_LOW
    # # Opening travel day
    # total += travel_cost
    # total += full_cost * max(((current_project.end_date - current_project.start_date).days - 1),0)
    # # TODO Determine status of the final day of the project
    # for n in range(next_project_index, len(list_of_strings)):
    #     if (next_project.start_date - current_project.end_date).days > 1:
    #         # End of previous 
    #         total += travel_cost
    #     current_project = next_project
    #     travel_cost = TRAVEL_DAY_HIGH if current_project.is_high_cost else TRAVEL_DAY_LOW
    #     full_cost = FULL_DAY_HIGH if current_project.is_high_cost else FULL_DAY_LOW
    #     total += (full_cost * (current_project.end_date - current_project.start_date).days)
    #     next_project_index += 1
    #     next_project = Project.from_string(list_of_strings[n])
    # final_project = Project.from_string(list_of_strings[-1])
    # total += travel_cost
    # if (current_project.end_date - final_project.start_date).days > 1:
    #     # Closing travel date
    #     total += travel_cost
    # total += full_cost * final_project.duration
    # return total    
            
