from datetime import datetime, timedelta
from pytz import timezone

dining_hall_list = ['Arrillaga', 'Branner', 'EVGR', 'FlorenceMoore', 'GerhardCasper', 'Lakeside', 'Ricker', 'Stern', 'Wilbur']

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

# Creates dates array
def generate_date_array():
    # Setup timezones for PST to ensure continuity
    pst_timezone = timezone('America/Los_Angeles')
    pst_now = datetime.now(pst_timezone)

    # Create an array for next 7 days
    date_array = [(pst_now + timedelta(days=i)).strftime('%m/%d/%Y').lstrip("0").replace("/0", "/") for i in range(7)]
    
    return date_array

dates_list = generate_date_array()