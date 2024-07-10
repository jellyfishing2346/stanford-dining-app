import time
import csv
from datetime import datetime
from pytz import timezone

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 

from dining_info import *


# Method to locate dropdown
def find_dropdown(id_name):
    # Construct dropdown ID
    dropdown_id = f'MainContent_lst{id_name}'
    
    # Wait for the dropdown to be present and return it
    dropdown = WebDriverWait(driver, 5, 100).until(
        EC.presence_of_element_located((By.ID, dropdown_id))
    )

    return dropdown

# Method to locate item in dropdown
def select_in_dropdown(id_name):
    # Construct the dropdown ID selector
    item_id = f'#MainContent_lst{id_name} option[selected="selected"]'

    # Retrieve currently selected date
    item = WebDriverWait(driver, 5, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, item_id))
    ).get_attribute('value')

    return item


# INITIAL TIME AND DRIVER SETUP
# Setup timezones for PST to ensure continuity
pst_timezone = timezone('America/Los_Angeles')
pst_now = datetime.now(pst_timezone)

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
# Uncomment the next line to run in headless mode
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')

# Set up WebDriver using WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Reference link to online Stanford Dining menu
url = 'https://rdeapps.stanford.edu/dininghallmenu/'
driver.get(url)


# INITIALIZE PAGE AND LOAD DOM WITH DUMMY SETTINGS
dummy_date = pst_now.strftime('%m/%d/%Y').lstrip("0").replace("/0", "/")
dummy_meal = "Breakfast"
dummy_hall = "Arrillaga"

date_dropdown = driver.find_element(By.ID, 'MainContent_lstDay')
Select(date_dropdown).select_by_value(dummy_date)

dining_hall_dropdown = driver.find_element(By.ID, 'MainContent_lstLocations')
Select(dining_hall_dropdown).select_by_value(dummy_hall)

meal_type_dropdown = driver.find_element(By.ID, 'MainContent_lstMealType')
Select(meal_type_dropdown).select_by_value(dummy_meal)


# ITERATE THROUGH DATES, HALLS, AND MEALS
for date in dates_list:
    date_dropdown = find_dropdown('Day')

    # Select date from the dining hall dropdown
    Select(date_dropdown).select_by_value(date)

    selected_date = select_in_dropdown('Day')

    print("Fetching data for:", selected_date)

    for hall in dining_hall_list:
        dining_hall_dropdown = find_dropdown('Locations')

        # Select hall from the dining hall dropdown
        Select(dining_hall_dropdown).select_by_value(hall)

        selected_dining_hall = select_in_dropdown('Locations')

        print("Selected dining hall:", dining_hall_alias[selected_dining_hall])

        for meal in meal_type_list:
            meal_type_dropdown = find_dropdown('MealType')

            # Select meal from the meal type dropdown
            Select(meal_type_dropdown).select_by_value(meal)

            selected_meal_type = select_in_dropdown('MealType')

            print("Selected meal type:", selected_meal_type)


# Wait for user input before closing the browser
input("Press enter to close the browser...")
driver.quit()