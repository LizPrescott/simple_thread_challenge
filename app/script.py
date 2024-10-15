
from collections import namedtuple
from datetime import date
import app.constants as constants

Dates = namedtuple('Dates', ["name", "start_date", "end_date", "is_high_cost"])


def parse_date(date_string):
    month, day, year = date_string.strip().split("/")
    year = ("20" + year).split(" ")[0]
    return date(int(year), int(month), int(day))


def parse_input(string):
    name, cost_string, start_date_str, end_date_str = string.split(":")
    end_date = parse_date(end_date_str)
    start_date = parse_date(start_date_str)
    is_high_cost = "High" in cost_string
    return Dates(name, start_date, end_date, is_high_cost)


def calculate_project_cost(project, max_travel_days: int, max_full_days: int):
    high = project.is_high_cost
    if high:
        travel_day_cost = constants.TRAVEL_DAY_HIGH
        full_day_cost = constants.FULL_DAY_HIGH
    else:
        travel_day_cost = constants.TRAVEL_DAY_LOW
        full_day_cost = constants.FULL_DAY_LOW
    return ((max_full_days * full_day_cost) + (travel_day_cost * max_travel_days))


def base_case_full_days(project):
    full_days = project.end_date.day - project.start_date.day
    if full_days > 0:
        full_days -= 1
    return full_days


def project_overlap(current_project, next_project):
    return next_project.start_date.day - current_project.end_date.day


def calculate_reimbursement(list_of_strings):
    # Handles empty project sets
    if not list_of_strings:
        return
    current_project = parse_input(list_of_strings[0])
    # Single project is a special case
    if len(list_of_strings) == 1:
        return [
            {
                current_project.name: calculate_project_cost(current_project, 2, base_case_full_days(current_project))}
          ]
    results = []
    next_project_index = 1
    next_project = list_of_strings[next_project_index]
    while next_project:
        max_travel_days = 2
        max_full_days = base_case_full_days(current_project)
        next_project = parse_input(next_project)
        if current_project.end_date.day + 1 == next_project.start_date.day:
              max_travel_days -= 1
              max_full_days += 1
                
        cost = calculate_project_cost(
            current_project,
            max_full_days=max_full_days,
            max_travel_days=max_travel_days
            )
        results.append({current_project.name: cost})
        current_project = next_project
        next_project_index += 1
        # catch the index error on last project. Will not have a next project
        try:
            next_project = list_of_strings[next_project_index]
        except IndexError:
            # current project is now next and final project
            # TODO Handle second to last project has higher cost and overlaps
            cost = calculate_project_cost(current_project, 1, base_case_full_days(current_project))
            results.append({current_project.name: cost})
            break
    return results
