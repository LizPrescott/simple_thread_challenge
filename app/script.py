
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


def calculate_project_cost(project):
    high = project.is_high_cost
    if high:
        travel_day_cost = constants.TRAVEL_DAY_HIGH
        full_day_cost = constants.FULL_DAY_HIGH
    else:
        travel_day_cost = constants.TRAVEL_DAY_LOW
        full_day_cost = constants.FULL_DAY_LOW
    # TODO: Logic for contiguous projects in a set
    #  Minus 1 when the last day is a travel day, subtract that day
    full_days = project.end_date.day - project.start_date.day - 1
    return ((full_days * full_day_cost) + (travel_day_cost*2))


def calculate_reimbursement(list_of_strings):
    # Handles empty project sets
    if not list_of_strings:
        return
    current_project = parse_input(list_of_strings[0])
    cost = calculate_project_cost(current_project)
    #   if project.end_date == next.end_date:
    #     total_cost += full_day_cost
    return [{current_project.name: cost}]
