import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException,
    WebDriverException,
)

#browser = input("Enter your preferred browser (Firefox, Edge or Chrome): ")
webdriver_path = ChromeDriverManager().install()
email_address = "max.gapa+automation_tests@kenja.com"
password = "automation_testing1234"
os.environ["PATH"] += os.pathsep + webdriver_path

chrome_options = Options()
options = [
    #"--headless",
   #"--disable-gpu",
    #"--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

chrome_service = Service(webdriver_path)
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
# if browser.lower() == "firefox":
#     profile = webdriver.FirefoxProfile()
#     profile.accept_untrusted_certs = True
#     options = webdriver.FirefoxOptions()
#     options.binary_location = input(
#         "Since you're a firefox user, please input your firefox.exe location to avoid problems: "
#     )
#     driver = webdriver.Firefox(options=options)
# elif browser.lower() == "chrome":
#     options = webdriver.ChromeOptions()
#     options.add_argument("--ignore-certificate-errors")
#     driver = webdriver.Chrome(options=options)
# else:
#     raise Exception("Unsupported browser")

class Flow_create:
    def __init__(
        self,
        webdriver_path=webdriver_path,
        email_address=email_address,
        password=password,
        teardown=False,
    ):
        global driver
        self.driver = driver
        self.webdriver_path = webdriver_path
        self.email_address = email_address
        self.password = password
        self.wait = WebDriverWait(self.driver, 60)
        self.teardown = teardown
        self.image_path = ""
        os.environ["PATH"] += self.webdriver_path
        super(Flow_create, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def __enter__(self):
        return self

    def login(self):
        self.driver.get("https://r3qa-3.qarooms3.kenja.com/")
        self.driver.maximize_window()
        self.driver.execute_script("document.body.style.zoom='100%'")
        # Enter email address and password
        self.driver.find_element(By.ID, "login-input-email").send_keys(
            self.email_address
        )
        self.driver.find_element(By.ID, "login-input-password").send_keys(self.password)

        # Click login button
        self.driver.find_element(By.CSS_SELECTOR, ".btn-block").click()

        # Wait for login to complete
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".header-bottom-menu-add > .header-bottom-menu-item")
            )
        )

    def navigate_create_flow(self):
        #Click on flow button
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='kenjaicon kenjaicon-flow']"))
            ).click()
        #Click on rooms actions button
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(concat(' ', @class, ' '), 'header-bottom-menu-item') and contains(concat(' ', @class, ' '), 'dropdown-toggle')]"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Create a flow')]"))
        ).click()

    def create_first_flow(self):
        #Create a flow using a test template
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div[9]/div[3]/button[1]"))
        ).click()
        time.sleep(1)

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='dialog-step-1']/div[1]/input"))
            ).click()
        time.sleep(1)

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='dialog-step-1']/div[1]/input")
            )
        #Type name of a flow
        ).send_keys("flow_test")
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='dialog-next-button']"))
            ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//option[text() = 'Myszka Maksymilian']"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='dialog-next-button']"))
            ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='dialog-next-button']"))
            ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='content-container']/div/a"))
            ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='result-container']/div/div[1]/div[1]/div/span"))
        )
        time.sleep(0.5)
        if self.driver.find_element(By.XPATH, "//*[@id='result-container']/div/div[1]/div[1]/div/span").text  == "flow_test":
            self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='result-container']/div/div[1]/div[1]/div/div/a"))
            ).click()
            self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='result-container']/div/div[2]/div[1]/div/div/span[2]/button"))
            ).click()
            time.sleep(0.5)
            self.driver.switch_to.alert.accept()

bot = Flow_create()
if __name__ == "__main__":
    try:
        bot.login()
        bot.navigate_create_flow()
        bot.create_first_flow()
        
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
