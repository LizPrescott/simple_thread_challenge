
from datetime import date
from itertools import pairwise
from more_itertools import peekable # `pip install more-itertools`
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
        self.full_days = max((self.end_date - self.start_date).days - 1, 0)
        # +1 to account for opening days
        self.duration = (self.end_date - self.start_date).days + 1
        self.travel_days = min(2, self.duration)

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

    def replace_travel_day(self):
        self.travel_days -= 1
        self.full_days += 1

    def restore_travel_day(self):
        self.travel_days += 1
        self.full_days -= 1

    def calculate_project_cost(self):
        if self.is_high_cost:
            travel_day_cost = TRAVEL_DAY_HIGH
            full_day_cost = FULL_DAY_HIGH
        else:
            travel_day_cost = TRAVEL_DAY_LOW
            full_day_cost = FULL_DAY_LOW
        return max((self.full_days * full_day_cost) + (travel_day_cost * self.travel_days), 0)


def handle_opening_pair(first_project, second_project):
    project_overlap = (first_project.end_date - second_project.start_date).days + 1
    # Even if projects are contiguous, opening day is still a travel day
    if project_overlap == 0:
        second_project.replace_travel_day()
        if first_project.travel_days > 1:
            first_project.replace_travel_day()
    if project_overlap >= first_project.duration > 0:
        while first_project.travel_days > 0:
            first_project.replace_travel_day()
        while project_overlap > 0 and first_project.full_days > 0:
            first_project.full_days -= 1
            project_overlap -= 1


def handle_contiguous_projects(current_project, next_project):
    current_project.replace_travel_day()
    next_project.replace_travel_day()


def handle_overlap(current_project, next_project, project_overlap):
    if current_project.is_high_cost:
        donor_project = next_project
        safe_project = current_project
    else:
        donor_project = current_project
        safe_project = next_project
    if safe_project.travel_days > 0:
        safe_project.replace_travel_day()
    if donor_project.travel_days > 0:
        donor_project.travel_days -= 1
        project_overlap -= 1
    donor_project.full_days -= project_overlap
    # Need a test of overlapping low cost projects longer than a day


def calculate_reimbursement(list_of_strings):
    # Handles empty project sets
    if not list_of_strings:
        return
    project_set = Reimbursement(list_of_strings)
    starting_iter = peekable(iter(project_set))
    # Single project is a special case
    if len(list_of_strings) == 1:
        only_project = next(starting_iter)
        return only_project.calculate_project_cost()
    total = 0
    # Find opening travel day
    while total == 0:
        first_project = next(starting_iter)
        second_project = starting_iter.peek()
        handle_opening_pair(
            first_project,
            second_project
        )
        total = first_project.calculate_project_cost()
    # Iterator will have already exhausted first travel project
    for current_project, next_project in pairwise(starting_iter):
        project_overlap = (current_project.end_date - next_project.start_date).days + 1
        if project_overlap == 0:
            handle_contiguous_projects(current_project, next_project)
        if project_overlap > 0:
            handle_overlap(current_project, next_project, project_overlap)
        total += current_project.calculate_project_cost()
    final_project = project_set.projects[-1]
    if final_project.travel_days == 0:
        final_project.restore_travel_day()
    total += final_project.calculate_project_cost()
    return total
