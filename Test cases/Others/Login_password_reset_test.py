from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os


def test_valid_login_logout(driver, email_address, password):
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
    driver.find_element(By.LINK_TEXT, "Log out").click()
    driver.find_element(By.LINK_TEXT, "Lost Password?").click()
    driver.find_element(By.ID, "input-email").send_keys(email_address)
    driver.find_element(By.XPATH, "//input[@value='Reset Password']").click()
    try:
        element = driver.find_element(
            By.XPATH,
            "//p[contains(text(), 'Password reset instructions sent to your e-mail')]",
        )
        print("Test succeded")
    except:
        print("Password reset text didn't show up")


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

driver.get("https://kenja.rooms3.dvl/#")
driver.fullscreen_window()

try:
    test_valid_login_logout(driver, email_address, password)
except NoSuchElementException as e:
    print(f"Failed to find and/or use the element: {e}")
finally:
    print("Testing over. Congrats if you didn't get any errors!")
    driver.quit()
