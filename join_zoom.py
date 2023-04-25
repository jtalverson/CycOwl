from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import getpass
from pynput.keyboard import Key
import pynput.keyboard as keyboard
from pynput.mouse import Button
import pynput.mouse as mouse
import shelve

long_path = "/home/" + getpass.getuser() + "/CycOwl/"

shelf_path = long_path + "shelf/shelf"

shelf = shelve.open(shelf_path)
shelf["zoom_down"] = False
shelf["zoom_error"] = False
shelf.close()

def start_zoom():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option('prefs',{'profile.default_content_setting_values.media_stream_mic':1})


    meet_code = 8174831944

    # long_path = "/home/" + getpass.getuser() + "/CycOwl/"
    global driver
    driver = webdriver.Chrome(options=chrome_options) # create web driver
    actions = ActionChains(driver)

    driver.get('https://zoom.us/wc/' + str(meet_code) + '/start')
    # driver.fullscreen_window()
    # https://zoom.us/wc/8174831944/start

    chrome_button = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/div/div[2]/div/div[2]/div/div/a[3]")))
    #sleep(2)
    driver.execute_script("arguments[0].scrollIntoView(true);", chrome_button)
    chrome_button.click()
    #sleep(2)
    emailEL = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='identifierId']")))
    #emailEL = driver.find_element(By.XPATH, "//*[@id='identifierId']")
    shelf = shelve.open(shelf_path)
    shelf["status"] = "Entering credentials"
    shelf.close()
    emailEL.click()
    gmail = 'cycowlnano@gmail.com'
    emailEL.send_keys(gmail)
    emailEL.send_keys(Keys.RETURN)

    #sleep(2)
    password = 'cap2023!'
    passEL = WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")))
    #passEL= driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")
    passEL.click()
    passEL.send_keys(password)
    passEL.send_keys(Keys.RETURN)

    shelf = shelve.open(shelf_path)
    shelf["status"] = "Reclaiming host"
    shelf.close()
    claim_host = "/html/body/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/div[4]/div[1]/div/div[2]/button[2]"
    
    
    try:
        claim_host_button = WebDriverWait(driver, timeout=20).until(lambda d: d.find_element(By.XPATH, claim_host))
        claim_host_button.click()
        join_audio_other = "//*[@id='foot-bar']/div[1]/div[1]/button"
        other_join = WebDriverWait(driver, timeout=20).until(lambda d: d.find_element(By.XPATH, join_audio_other))
        other_join.click()
    except:
        pass

    try:
        global audiojoin
        join_audio_path = "//*[@id='voip-tab']/div/button"
        audiojoin = WebDriverWait(driver, timeout=25).until(EC.element_to_be_clickable((By.XPATH, join_audio_path)))
    except:
        print("validation required")
        shelf = shelve.open(shelf_path)
        shelf["status"] = "Error occurred, restarting"
        shelf.close()
        driver.close()
        start_zoom()

try:
    start_zoom()

    shelf = shelve.open(shelf_path)
    shelf["status"] = "Joined meeting"
    shelf.close()
    print("found join audio button at ")
    print(audiojoin.location)
    fail_to_join = True
    while fail_to_join:
        try:
            audiojoin.click()
            fail_to_join = False
        except:
            print("Could not click join audio, trying again")
            sleep(.1)

    shelf = shelve.open(shelf_path)
    shelf["status"] = "Sharing screen"
    shelf.close()
    sleep(.5)

    shelf = shelve.open(shelf_path)
    shelf["share_ready"] = True
    shelf.close()

    minimized = False
    while not minimized:
        shelf = shelve.open(shelf_path)
        minimized = shelf["minimized"]
        shelf.close()
        sleep(.1)

    print("screen minimized, ready to proceed")

    screenshare = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, "//*[@id='sharing-entry-button-container-dropdown']"))
    screenshare.click()

    keyboard = keyboard.Controller()

    keyboard.tap(Key.tab)
    sleep(.1)
    keyboard.tap(Key.right)
    sleep(.01)
    keyboard.tap(Key.tab)
    sleep(.01)
    keyboard.tap(Key.right)
    sleep(.01)
    keyboard.tap(Key.enter)

    shelf = shelve.open(shelf_path)
    shelf["share_started"] = True
    shelf.close()

    close = False
    while not close:
        shelf = shelve.open(shelf_path)
        close = shelf["stop"]
        shelf.close()
        sleep(.75)

    end_meeting = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, "//*[@id='foot-bar']/div[3]"))
    end_meeting.click()
    for_all = WebDriverWait(driver, timeout=30).until(lambda d: d.find_element(By.XPATH, "//*[@id='wc-footer']/div[2]/div[2]/div/div/button[1]"))
    for_all.click()

    shelf = shelve.open(shelf_path)
    shelf["zoom_down"] = True
    shelf.close()
    driver.close()
except Exception as e:
    print(e)
    print("error occurred while loading zoom")
    driver.close()
    shelf = shelve.open(shelf_path)
    shelf["zoom_down"] = True
    shelf["zoom_error"] = True
    shelf.close()