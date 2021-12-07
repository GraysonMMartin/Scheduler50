from flask import redirect, render_template, session
from functools import wraps

from datetime import datetime, timedelta

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    # Adapted from CS50 Finance problem set
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def valid_date(start_date,end_date):
    """
    Check if the user enter's a valid date
    """
    # Note that in the html input I have made the minimum value as today's date
    # Therefore I only need to check if the end date is before the start date

    start_date_dateform = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dateform = datetime.strptime(end_date, '%Y-%m-%d')

    if (end_date_dateform - start_date_dateform).days < 0:
        return False
        
    return True

def all_dates(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    dates = []
    delta = timedelta(days=1)
    while start_date <= end_date:
        dates.append(start_date.strftime('%Y-%m-%d'))
        start_date += delta
    return dates

