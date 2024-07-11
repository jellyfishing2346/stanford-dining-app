from datetime import datetime, timedelta
from pytz import timezone

dining_hall_list = [
    'Arrillaga', 'Branner', 'EVGR', 'FlorenceMoore', 
    'GerhardCasper', 'Lakeside', 'Ricker', 'Stern', 'Wilbur'
]

dining_hall_alias = {
    'Arrillaga': 'Arrillaga Family Dining Commons',
    'Branner': 'Branner Dining',
    'EVGR': 'EVGR Dining',
    'FlorenceMoore': 'Florence Moore Dining',
    'GerhardCasper': 'Gerhard Casper Dining',
    'Lakeside': 'Lakeside Dining',
    'Ricker': 'Ricker Dining',
    'Stern': 'Stern Dining',
    'Wilbur': 'Wilbur Dining'
}

meal_type_list = ['Breakfast', 'Lunch', 'Dinner', 'Brunch']

def generate_date_array():
    """
    Generate an array of dates for the next 7 days in m/d/yyyy format
    """
    pst_timezone = timezone('America/Los_Angeles')
    pst_now = datetime.now(pst_timezone)
    return [(pst_now + timedelta(days=i)).strftime('%m/%d/%Y').lstrip("0").replace("/0", "/") for i in range(7)]

dates_list = generate_date_array()