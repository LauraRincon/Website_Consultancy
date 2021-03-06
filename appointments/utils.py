from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Project, Client

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar,self).__init__()

    def formatday(self, day, events):
        events_per_day = Project.objects.filter(appt_date__day=day)
        d = ''
        # Obtain appointments day for the projects
        for event in events_per_day:
            d = f'reserved'
        # Stylish days with events
        if day != 0:
            if d:
                return f"<td class='table-success'>{day}\n <p id='table'> {d} </p></td>" #'
            else:
                return f"<td>{day}</td>"
        # Days of near months are empty
        return f'<td> </td>'

    def formatweek(self, theweek, events):
        week = ''
        # Obtain formartdar per week, in the month
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        # Get the proyects with appointments in the current year and month.
        events = Project.objects.filter(appt_date__year=self.year, appt_date__month=self.month)

        # Build and filled calendar table
        cal =  "<div>\n" 
        cal += f"<table class='table table-bordered'>\n"
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal +=  "</tdbody>\n</table>\n</div>\n"
        return cal
