import pickle
import time
import csv
from progress.bar import IncrementalBar
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

SCROLL_PAUSE_TIME = 1.0

# options = Options()
# options.set_headless(headless = False)

# Workaround since latest geckodriver and Firefox versions do not completely support Selenium
# capabilities = webdriver.DesiredCapabilities().FIREFOX
# capabilities["marionette"] = True

# firefox_profile = FirefoxProfile()
# ## Disable images
# firefox_profile.set_preference('permissions.default.image', 2)
CHROMEDRIVER_PATH = r'/Volumes/nikhil_t7/Python/Bots/chromedriver'
driver = webdriver.Chrome(CHROMEDRIVER_PATH)
# cookies

cookies_file_path = '/Volumes/nikhil_t7/Python/Bots/LinkedIn-2/cookies.pkl'


def save_cookie(path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


driver.get("https://www.linkedin.com")


def load_cookie(path):
    try:
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except Exception as e:
        print(e)
        #replace  empty string [""] with your username and password of Linkedin Account.
        username = ""
        password = ""
        driver.find_element_by_id('session_key').send_keys(username)
        driver.find_element_by_id('session_password').send_keys(password)
        driver.find_element_by_class_name(
            'sign-in-form__submit-button').click()
        save_cookie(path)


load_cookie(cookies_file_path)

driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections")


def scrollToBottom():
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # try:
        #     elem = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[2]/div/button")
        #     elem.click()
        # except NoSuchElementException:
        #     print("more button not available")
        #     pass
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script("window.scrollTo(0,0);")
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height


scrollToBottom()
cards = driver.find_elements_by_class_name('mn-connection-card__link')
print(len(cards))
links = []

for card in cards:
    links.append(card.get_attribute('href'))
with open("connections.csv" + time.asctime(time.localtime(time.time())), "w", newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        'Link'])
    writer.writeheader()

    bar = IncrementalBar('Fetching Connections', max=len(links))
    print(len(links))
    for link in links:

        driver.get(link + "details/skills/")
        time.sleep(SCROLL_PAUSE_TIME)
        try:
            elements = driver.find_elements_by_xpath("//span[text()='Endorse']")
            try:
                endorsedElement = driver.find_element_by_xpath("//span[text()='Endorsed']")
                driver.execute_script("arguments[0].scrollIntoView();", endorsedElement)
            except Exception as e:
                print(e, "no skills endorsed yet")
                pass
            for element in elements:
                element.click()
        except Exception as e:
            print(e, "no skills left to endorse")
            pass
        writer.writerow({'Link': link})
        bar.next()

    bar.finish()
    driver.close()
