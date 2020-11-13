from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Project

class Calendar(HTMLCalendar):
    def __init__(self, id=None, year=None, month=None):
        self.year = year
        self.month = month
        self.id = id
        super(Calendar,self).__init__()

    def formatday(self, id, day, events):
        events_per_day = Project.objects.filter(client__id= self.id, appt_date__day=day)
        d = ''
        for event in events_per_day:
            d = f'<p>reserved</p>'
        if day != 0:
            if d:
                return f"<td class='table-primary'>{day}<span> {d} </span></td>"
            else:
                return f"<td>{day}</td>"
        return f'<td> </td>'

    def formatweek(self, id, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(id, d, events)
        return f'<tr> {week} </tr>'
    
    def formatmonth(self, id, withyear=True):
        events = Project.objects.filter(client__id= self.id, appt_date__year=self.year, appt_date__month=self.month)
        cal =  "<div class='table-responsive-sm'>\n"
        cal += f"<table class='table table-bordered'>\n" #f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'

        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(id, week, events)}\n'
        cal +=  "\n</div>"
        return cal



