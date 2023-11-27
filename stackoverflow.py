from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium import webdriver

import time
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
from selenium.common.exceptions import NoSuchElementException

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# URL of the page containing user profiles
url = "https://stackoverflow.com/users"
response = driver.get(url)
time.sleep(5)
query="react"
driver.find_element(By.XPATH,"//input[@id='userfilter']").send_keys(query)
time.sleep(8)
#find block with all users
users=driver.find_element(By.ID,"user-browser")

# Open a CSV file for writing
with open('user_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Define the CSV writer
    csv_writer = csv.writer(csvfile)

    # Write header row
    csv_writer.writerow(['Username', 'Location', 'Reputation Score', 'User Tags', 'Profile Picture URL'])
    
    while True:
        # Find all div elements with class "grid--item user-info"
        user_info_divs = driver.find_elements(By.CLASS_NAME, "grid--item.user-info")

        # Iterate over each div and extract information
        for user_info_div in user_info_divs:
            # Extract information from the current div
            user_gravatar_div = user_info_div.find_element(By.CLASS_NAME, "user-gravatar48")
            profile_pic_url = user_gravatar_div.find_element(By.TAG_NAME, "img").get_attribute("src")
            
            user_details = user_info_div.find_element(By.CLASS_NAME, "user-details")
            username = user_details.find_element(By.TAG_NAME, "a").text
            
            user_location = user_info_div.find_element(By.CLASS_NAME, "user-location").text
            
            reputation_score = user_info_div.find_element(By.CLASS_NAME, "reputation-score").text
            
            user_tags = user_info_div.find_element(By.CLASS_NAME, "user-tags").text
            
            # Write the information to the CSV file
            csv_writer.writerow([username, user_location, reputation_score, user_tags, profile_pic_url])

        try:
            # Find and click the "Next" link to go to the next page
            next_page_link = driver.find_element(By.XPATH, "//a[@rel='next']")
            next_page_link.click()
            time.sleep(3)

        except NoSuchElementException:
            # No "Next" link found, exit the loop
            print("No more pages available. Exiting.")
            break

