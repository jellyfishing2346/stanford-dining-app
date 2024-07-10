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

# Wait for date dropdown to be present 
date_dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'MainContent_lstDay'))
)

Select(date_dropdown).select_by_value(dummy_date)

# Wait for dining hall dropdown to be present
dining_hall_dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'MainContent_lstLocations'))
)

Select(dining_hall_dropdown).select_by_value(dummy_hall)

# Wait for the meal type dropdown to be present
meal_type_dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'MainContent_lstMealType'))
)

Select(meal_type_dropdown).select_by_value(dummy_meal)


# Iterate through halls and meals for specific date
print("Fetching data for:", dummy_date)
for hall in dining_hall_list:
    # Wait for the dining hall dropdown to be present
    dining_hall_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'MainContent_lstLocations'))
    )

    # Select dining_hall from the dining hall dropdown
    Select(dining_hall_dropdown).select_by_value(hall)

    # Retrieve currently selected dining hall
    selected_dining_hall = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#MainContent_lstLocations option[selected="selected"]'))
    ).get_attribute('value')

    print("Selected dining hall:", dining_hall_alias[selected_dining_hall])

    for meal in meal_type_list:
        # Wait for the meal type dropdown to be present
        meal_type_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'MainContent_lstMealType'))
        )

        # Select meal_type from the meal type dropdown
        Select(meal_type_dropdown).select_by_value(meal)

        # Retrieve currently selected meal type
        selected_meal_type = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#MainContent_lstMealType option[selected="selected"]'))
        ).get_attribute('value')

        print("Selected meal type:", selected_meal_type)
    
    time.sleep(1)


# Wait for user input before closing the browser
input("Press enter to close the browser...")
driver.quit()