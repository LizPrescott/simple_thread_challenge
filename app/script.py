
from datetime import date
from itertools import pairwise
from more_itertools import peekable
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

    def calculate(self):
        # Handles empty project sets
        if not self.projects:
            return 0
        project_set = self.projects
        starting_iter = peekable(iter(project_set))
        # Single project is a special case
        if len(project_set) == 1:
            only_project = next(starting_iter)
            return only_project.calculate_project_cost()
        total = 0
        # Find opening travel day
        while total == 0:
            first_project = next(starting_iter)
            second_project = starting_iter.peek()
            ProjectPair(first_project, second_project).handle_opening_pair()
            total = first_project.calculate_project_cost()
        # Iterator will have already exhausted first travel project
        for current_project, next_project in pairwise(starting_iter):
            ProjectPair(current_project, next_project).resolve()
            total += current_project.calculate_project_cost()
        final_project = project_set[-1]
        if final_project.travel_days == 0:
            final_project.restore_travel_day()
        total += final_project.calculate_project_cost()
        return total


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

    def swap_out_travel_day(self):
        self.travel_days -= 1
        self.full_days += 1

    def restore_travel_day(self):
        self.travel_days += 1
        self.full_days -= 1

    def decrement_all_days(self, decrement_by):
        while self.travel_days > 0:
            self.swap_out_travel_day()
        while decrement_by > 0 and self.full_days > 0:
            self.full_days -= 1
            decrement_by -= 1

    def calculate_project_cost(self):
        if self.is_high_cost:
            travel_day_cost = TRAVEL_DAY_HIGH
            full_day_cost = FULL_DAY_HIGH
        else:
            travel_day_cost = TRAVEL_DAY_LOW
            full_day_cost = FULL_DAY_LOW
        return max(
            sum([  # Careful here
                # Use list instead of set, to avoid the dedup behavior of sets
                (self.full_days * full_day_cost),
                (travel_day_cost * self.travel_days)
                                                 ]), 0
            )


class ProjectPair:
    def __init__(self, project_a, project_b):
        self.overlap = self.__overlap(project_a, project_b)
        self.donor_project = project_b if project_a.is_high_cost else project_a
        self.safe_project = project_a if project_a.is_high_cost else project_b
        self.contiguous = self.overlap == 0

    @staticmethod
    def __overlap(project_a, project_b):
        return (project_a.end_date - project_b.start_date).days + 1

    def handle_opening_pair(self):
        if self.contiguous:
            self.handle_contiguous_projects(1)
        elif self.overlap >= self.donor_project.duration > 0:
            self.donor_project.decrement_all_days(self.overlap)
        elif self.overlap >= 0:
            self.handle_overlap(1)

    def handle_contiguous_projects(self, min_travel_days=0):
        if self.donor_project.travel_days > min_travel_days:
            self.donor_project.swap_out_travel_day()
        if self.safe_project.travel_days > min_travel_days:
            self.safe_project.swap_out_travel_day()

    def handle_overlap(self, min_travel_days=0):
        if self.safe_project.travel_days > min_travel_days:
            self.safe_project.swap_out_travel_day()
        if self.donor_project.travel_days > min_travel_days:
            self.donor_project.travel_days -= 1
            self.overlap -= 1
        self.donor_project.full_days = max(
            self.donor_project.full_days - self.overlap, 0
            )

    def resolve(self):
        if self.contiguous:
            self.handle_contiguous_projects()
        elif self.overlap >= self.donor_project.duration > 0:
            self.safe_project.swap_out_travel_day()
            self.donor_project.decrement_all_days(self.overlap)
        elif self.overlap > 0:
            self.handle_overlap()
