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

# Setup timezones for PST to ensure continuity
pst_timezone = timezone('America/Los_Angeles')
pst_now = datetime.now(pst_timezone)

# SETUP VARIABLES FOR TEMPORARY TESTING
todays_date = pst_now.strftime('%m/%d/%Y').lstrip("0").replace("/0", "/")
meal_type = "Breakfast"
dining_hall = "Arrillaga"

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
# Uncomment the next line to run in headless mode
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-extensions')

# Set up WebDriver using WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = 'https://rdeapps.stanford.edu/dininghallmenu/'
driver.get(url)

# Wait for the date dropdown to be present
date_dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'MainContent_lstDay'))
)

# Retrieve currently selected date
selected_date = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#MainContent_lstDay option[selected="selected"]'))
).get_attribute('value')

# Convert selected date format to match today's date format
selected_date_converted = selected_date.split(' - ')[0]

print("Dates match:", selected_date_converted == todays_date)

# ------------------------------------------------------------------------------------------------- #

for hall in dining_hall_list:
    # Wait for the dining hall dropdown to be present
    dining_hall_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'MainContent_lstLocations'))
    )

    # Select dining_hall from the dining hall dropdown
    Select(dining_hall_dropdown).select_by_value(hall)
    
    # Retrieve currently selected dining hall
    selected_dining_hall = Select(dining_hall_dropdown).first_selected_option.get_attribute('value')
    
    print("Selected dining hall:", dining_hall_alias[selected_dining_hall])

    for meal in meal_type_list:
        # Wait for the meal type dropdown to be present
        meal_type_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'MainContent_lstMealType'))
        )

        # Select meal_type from the meal type dropdown
        Select(meal_type_dropdown).select_by_value(meal)

        # Retrieve currently selected meal type // using this method because stale element when trying method in line 61
        selected_meal_type = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#MainContent_lstMealType option[selected="selected"]'))
        ).get_attribute('value')

        print("Selected meal type:", selected_meal_type)
    
    # Close instance of WebDriver and reinstate to stop stale element
    driver.quit()
    time.sleep(0.5)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

# ------------------------------------------------------------------------------------------------- #

# Wait for user input before closing the browser
input("Press enter to close the browser...")
driver.quit()