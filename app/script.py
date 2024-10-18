
from datetime import date, timedelta
import app.constants as constants


class ProjectSet:
    def __init__(self, input_list):
        self.length = len(input_list)


class Project:
    def __init__(self, name, start_date, end_date, is_high_cost):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.is_high_cost = is_high_cost
        self.travel_days = 2
        self.full_days = (self.end_date - self.start_date).days - 1

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
            travel_day_cost = constants.TRAVEL_DAY_HIGH
            full_day_cost = constants.FULL_DAY_HIGH
        else:
            travel_day_cost = constants.TRAVEL_DAY_LOW
            full_day_cost = constants.FULL_DAY_LOW
        return (self.full_days * full_day_cost) + (travel_day_cost * self.travel_days)

    def project_overlap(self, next_project):
        return next_project.start_date.day - self.end_date.day + 1
   
    def handle_final_project(self):
        pass


def calculate_reimbursement(list_of_strings):
    # Handles empty project sets
    if not list_of_strings:
        return
    current_project = Project.from_string(list_of_strings[0])
    # Single project is a special case
    if len(list_of_strings) == 1:
        return [
            {
                current_project.name: current_project.calculate_project_cost()}
          ]
    results = []
    next_project_index = 1
    next_project = list_of_strings[next_project_index]
    while next_project:
        next_project = Project.from_string(next_project)
        project_overlap = current_project.project_overlap(next_project)
        if (next_project.start_date - current_project.end_date).days == 1:
            current_project.remove_travel_day()
            next_project.remove_travel_day()
        elif current_project.end_date >= next_project.start_date:
            current_project.remove_travel_day()
            next_project.remove_travel_day()
            project_overlap = current_project.project_overlap(next_project)
            if current_project.is_high_cost:
                next_project.full_days -= project_overlap
            else:
                current_project.full_days -= project_overlap
        cost = current_project.calculate_project_cost()
        results.append({current_project.name: cost})
        current_project = next_project
        next_project_index += 1
        # catch the index error on last project. Will not have a next project
        try:
            next_project = list_of_strings[next_project_index]
        except IndexError:
            # current project is now next and final project
            # TODO Handle second to last project has higher cost and overlaps
            cost = current_project.calculate_project_cost()
            results.append({current_project.name: cost})
            break
    return results
