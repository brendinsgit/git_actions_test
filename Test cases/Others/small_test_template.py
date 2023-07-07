from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)
import os
import time


def test_valid_login(driver, email_address, password):
    # Enter email address and password
    driver.find_element(By.ID, "login-input-email").send_keys(email_address)
    driver.find_element(By.ID, "login-input-password").send_keys(password)

    # Click login button
    driver.find_element(By.CSS_SELECTOR, ".btn-block").click()

    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".header-bottom-menu-add > .header-bottom-menu-item")
        )
    )
    time.sleep(5)


browser = input("Enter your preferred browser (Firefox, Edge or Chrome): ")
webdriver_path = input("Enter the path to your webdriver: ")
email_address = input("Please provide an email that can be used to log in: ")
password = input("Please provide a password that can be used to log in: ")
os.environ["PATH"] += os.pathsep + webdriver_path

if browser.lower() == "firefox":
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True
    options = webdriver.FirefoxOptions()
    options.binary_location = input(
        "Since you're a firefox user, please input your firefox.exe location to avoid problems: "
    )
    driver = webdriver.Firefox(options=options)
elif browser.lower() == "chrome":
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=options)
else:
    raise Exception("Unsupported browser")

driver.get("https://r3qa-3.qarooms3.kenja.com/")
driver.maximize_window()
driver.execute_script("document.body.style.zoom='100%'")

try:
    test_valid_login(driver, email_address, password)
except NoSuchElementException as e:
    print(f"Failed to find and/or use the element: {e.msg}")
except ElementNotInteractableException as e:
    print(f"Failed to interact with the element: {e.msg}")
except TimeoutException as e:
    print(f"Timed out waiting for element: {e.msg}")
except StaleElementReferenceException as e:
    print(f"Element is no longer attached to the DOM: {e.msg}")
except WebDriverException as e:
    print(f"An error occurred while interacting with the WebDriver: {e.msg}")
finally:
    print("Testing over. Congrats if you didn't get any errors!")
    driver.quit()
