from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import getpass

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option('prefs',{'profile.default_content_setting_values.media_stream_mic':1})


meet_code = 8174831944

long_path = "/home/" + getpass.getuser() + "/CycOwl/"
driver = webdriver.Chrome(options=chrome_options) # create web driver
actions = ActionChains(driver)

driver.get('https://zoom.us/wc/' + str(meet_code) + '/start')
# driver.fullscreen_window()


el = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, "//*[@id='app']/div/div[2]/div/div[2]/div/div/a[3]"))
sleep(2)
driver.execute_script("arguments[0].scrollIntoView(true);", el)
el.click()
sleep(2)
emailEL= driver.find_element(By.XPATH, "//*[@id='identifierId']")
emailEL.click()
gmail = 'cycowlnano@gmail.com'
emailEL.send_keys(gmail)
emailEL.send_keys(Keys.RETURN)

sleep(2)
password = 'cap2023!'
passEL= driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")
passEL.click()
passEL.send_keys(password)
passEL.send_keys(Keys.RETURN)




audiojoin = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, "//*[@id='voip-tab']/div/button"))
print("found join audio button at ")
print(audiojoin.location)
audiojoin.click()


screenshare = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, "//*[@id='sharing-entry-button-container-dropdown']"))
screenshare.click()

window = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.Text, "//*[@id='sharing-entry-button-container-dropdown']"))


