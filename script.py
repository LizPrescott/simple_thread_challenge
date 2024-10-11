
from datetime import date

Dates = namedtuple('Dates', ["name", "start_date", "end_date", "is_high_cost?"]

def parse_input(self, string):
  name, cost_string, _, start_date_str, _, end_date_str = string.split(":")
  name = partition[0]
  end_date = self.parse_date(start_date_str)
  start_date = self.parse_date(start_date_str)
  is_high_cost = "High" in cost_string
  return Dates(name, start_date, end_date)


def parse_date(, date_string):
  month, day, year = date_string.strip().split("/")
  year = "20" + year
  return date(int(year), int(month), int(day))
