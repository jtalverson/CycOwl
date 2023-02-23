from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

meet_code = 4062239841

driver = webdriver.Chrome() # create web driver
actions = ActionChains(driver)

driver.get('https://zoom.us/wc/join/' + str(meet_code) + '?from=join')
# driver.fullscreen_window()

el = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, "//*[@id='nameInfo']"))
sleep(2)
driver.execute_script("arguments[0].scrollIntoView(true);", el)
list = driver.find_elements_by_xpath("//*[@id='onetrust-banner-sdk']/div/div/div[1]/button")
if len(list) > 0:
    list[0].click()
sleep(2)
name = 'Jetson'
driver.find_element_by_xpath("//input[@id='inputname']").send_keys(name)
sleep(2)
driver.find_element_by_xpath("//*[@id='joinBtn']").click()

el = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, "//*[@label='join audio']"))
print("found join audio button at ")
print(el.location)
el.click()
sleep(2)
el = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, "//*[@label='unmute my microphone']"))
print("found mute button at ")
print(el.location)
el.click()

driver.find_element_by_xpath("//*[@id='sharing-entry-button-container-dropdown']").click()


#sleep(5)
#driver.find_element_by_xpath("//input[@id='join-confno']").send_keys(meet_code)
#sleep(2)
#driver.find_element_by_xpath("//*[@id='onetrust-banner-sdk']/div/div/div[1]/button").click()
#sleep(2)
#driver.find_element_by_xpath("//a[@id='btnSubmit']").click()
#sleep(5)
# driver.find_element_by_xpath("//*[@id='zoom-ui-frame']/div[2]/div/div[1]/div").send_keys(Keys.ENTER)
#actions.send_keys(Keys.ENTER)
#actions.perform()
