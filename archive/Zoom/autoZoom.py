from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


# Meeting details
meeting_number = '9886355731'
display_name = 'Nano'
meeting_password = '9F2Fri'  # Leave empty if there's no password

# Create a new instance of the WebDriver 
driver = webdriver.Chrome()

# Open the localhost webpage
driver.get('http://localhost:3000')

# Wait for the page to load
time.sleep(3)

# Fill in the meeting number, display name, and password
driver.find_element_by_id('meeting-number').send_keys(meeting_number)
driver.find_element_by_id('display-name').send_keys(display_name)
driver.find_element_by_id('meeting-password').send_keys(meeting_password)

# Submit the form
driver.find_element_by_css_selector('#join-meeting-form button[type="submit"]').click()

# Keep the browser open
time.sleep(30)

# Close the browser
driver.quit()
