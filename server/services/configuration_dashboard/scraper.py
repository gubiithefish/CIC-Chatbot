from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep


def scraping(website: str):
    """Method to scrape a website... Nice docstring"""
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path="/Users/emilreinert/Documents/chromedriver")
    driver.get(website)

    # Let the website load
    sleep(8)

    # Clear cookie
    driver.find_element(by=By.XPATH, value='//*[@id="declineButton"]').click()

    # Get the page and find the related ID's
    sleep(4)
    source = driver.page_source
    limits = {"start": 'related="', "stop": '"><!'}
    _prior = source[source.find(limits['start']) + len(limits['start']):]
    _after = _prior[:_prior.find(limits['stop'])]
    return [_after]
