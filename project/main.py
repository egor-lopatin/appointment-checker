#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import os
import sys
import time
import random
import logging


def get_config_from_env_vars():
    return {
        "url": os.environ.get("SITE_URL"),
        "province": os.environ.get("PROVINCE"),
        "option_id": os.environ.get("OPTION_VALUE"),
        "user_id": os.environ.get("USER_ID"),
        "user_name": os.environ.get("USER_NAME"),
        "text_to_parse": os.environ.get("TEXT_TO_PARSE"),
    }


def random_user_agent():
    with open("user-agents.txt") as f:
        user_agents = f.readlines()
        return random.choice(user_agents).strip()


def driver_path():
    if os.environ.get("CHROME_DRIVER_PATH"):
        logging.info(
            "Chrome driver set with CHROME_DRIVER_PATH env var: %s",
            os.environ.get("CHROME_DRIVER_PATH"),
        )
        return ChromeService(executable_path=os.environ.get("CHROME_DRIVER_PATH"))
    else:
        logging.info(
            "Chrome driver not set with CHROME_DRIVER_PATH env var. Using webdriver-manager."
        )
        return ChromeService(ChromeDriverManager().install())


def load_driver(user_agent):
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=driver_path(), options=options)

    driver.set_window_size(1920, 1080)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride",
        {"userAgent": user_agent},
    )

    return driver


def close_driver(driver):
    driver.quit()


def make_screenshot(driver, page):
    # create directory if not exists
    if not os.path.exists(".screenshots"):
        os.makedirs(".screenshots")

    driver.save_screenshot(".screenshots/%s_page_screenshot.png" % page)


def is_appointment_available(driver, text_to_parse):
    if text_to_parse in driver.page_source:
        return False

    return True


def main(config, driver):
    logging.info(f"Loading page: {config['url']}")
    driver.get(config["url"])
    time.sleep(1)

    # Accept cookies if they appear
    logging.info("Accepting cookies")
    driver.find_element("id", "cookie_action_close_header").click()
    time.sleep(1)

    # Select the province
    logging.info(f"Selecting province: {config['province']}")
    drop = Select(driver.find_element("id", "form"))
    drop.select_by_visible_text(config["province"])
    time.sleep(1)

    driver.find_element("id", "btnAceptar").click()
    time.sleep(1)

    # Select the appointment option
    logging.info(f"Selecting appointment option: {config['option_id']}")
    drop = Select(driver.find_element("id", "tramiteGrupo[1]"))
    drop.select_by_value(config["option_id"])
    time.sleep(1)

    driver.find_element("id", "btnAceptar").click()

    # Accept the terms
    logging.info("Accepting terms")
    driver.find_element("id", "btnEntrar").click()
    time.sleep(1)

    # Fill the form
    logging.info("Submitting the form")
    driver.find_element("id", "txtIdCitado").send_keys(config["user_id"])
    driver.find_element("id", "txtDesCitado").send_keys(config["user_name"])
    time.sleep(1)

    driver.find_element("id", "btnAceptar").click()
    time.sleep(1)

    # Choose the appointment action
    logging.info("Choosing the appointment action")
    driver.find_element("id", "btnEnviar").click()
    time.sleep(1)

    # Check if appointment is available by parsing the page
    if is_appointment_available(driver, config["text_to_parse"]):
        logging.info(f"Appointment is available in {config['province']}. Go for it!")
        make_screenshot(driver, "available_appointment")
        # Let's exit with error code 1 to notify the user
        sys.exit(1)
    else:
        logging.info("Appointment is not available. Try again later.")
        sys.exit(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = get_config_from_env_vars()

    logging.info("Starting selenium driver")
    driver = load_driver(random_user_agent())

    try:
        main(config, driver)
    except Exception as e:
        logging.error(f"Error: {e}")

        if driver:
            make_screenshot(driver, "error")
            close_driver(driver)
