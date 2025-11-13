# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005CAB2087A1517C573F1218CF693C688D26493716082BB8E8DDBF1E25E5C2D27676401B9F0D16C82A3CCCEEBB257A45E88F892B519A8CC55C510081DE5AAF3079C319A70D0526A45C41206D16DB14955C3CC8BCA7BFCB80D61E7D4B5484A21E9B778419CA508005973D137BA4417ACED59CFD69C23C6B44B52398494911538A659CA11C75BDA251A35BFF439EAA911D3CFC98F43E6F45322A3578896A495C6F1713B375DF6D4B745D7DA60AE1B3FE524D5747A57D791688052D29E3AC6D372E8809D9C8ABC2C2E3469222C1DBCFE8895DAA81CEA02069B4E698E786744BE1094178723157EFCB713DA3431E086A44011E6F193233017A70D866B7819F4C25240EDFA8756331EDF44B36A2DF3BA0248499C2BCEEEEEBA917662463F13A2677DFAD25171E29AD45C53A886843A44B86824D3CAEBC911EF6AD78479DD43C98CCE45B8A418939A89B5139B5085C529DAD44A65D1622AC3CA4E53292FF1311CE9B5E1A7846A79C947E83D63F03A31C7D8F8340F18099E5FB65DF7F5BADB3BE674BF736EEB3230FE45FF28847B67D7D71AB22A1"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
