import os
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException


webdriver_path = ChromeDriverManager().install()
os.environ["PATH"] += os.pathsep + webdriver_path
file_path = os.path.abspath("./TestFiles/TheWondersOfNature.txt")
chrome_options = Options()
options = [
    # "--headless",
    #"--disable-gpu",
    #"--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--remote-debugging-port=9222"
]
for option in options:
    chrome_options.add_argument(option)

chrome_service = Service(webdriver_path)
driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))


class Searchbar_test:
    def __init__(
        self,
        webdriver_path=webdriver_path,
        email_address="max.gapa+automation_tests@kenja.com",
        password="automation_testing1234",
        teardown=False,
    ):
        self.driver = driver
        self.webdriver_path = webdriver_path
        self.email_address = email_address
        self.password = password
        self.teardown = teardown
        self.file_path = file_path
        self.wait = WebDriverWait(self.driver, 500)
        os.environ["PATH"] += self.webdriver_path
        super(Searchbar_test, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def __enter__(self):
        return self

    def login(self):
        print("Setting up the tests...")
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

    def go_into_TESTdpt(self):
        self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Private Rooms"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'TEST dpt')]"))
        ).click()

    def create_task(self, task_name):
        # Wait for the modal-backdrop fade to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        # Click on tasks tab
        element = self.driver.find_element(By.CSS_SELECTOR, "div[data-toggle='tasks']")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        # Click on "Add new task"
        driver.find_element(By.LINK_TEXT, "Add new task").click()
        # Set the name
        self.wait.until(EC.element_to_be_clickable((By.ID, "data-name"))).send_keys(
            task_name
        )
        # Find the select element
        select_element = driver.find_element(By.ID, "data-priority")

        # Create a Select object
        select_object = Select(select_element)

        # Select the "High" option
        select_object.select_by_visible_text("High")
        # Click all 3 checkboxes
        driver.find_element(By.NAME, "data[requires_acknowledge]").click()
        driver.find_element(By.NAME, "data[requires_approve]").click()
        driver.find_element(By.NAME, "data[requires_review]").click()
        # TO DO: SEND KEYS TO DESCRIPTION IF POSSIBLE
        # Click on add task
        driver.find_element(By.XPATH, "//button[text()='Add task']").click()

    def create_room(self, title, description):
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[@class='form-overlay']")
            )
        )
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal fade"))
        )
        # Wait for the modal-backdrop fade to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "glyphicon-plus"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Add sub room')]")
            )
        ).click()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "data[name]"))).send_keys(
            title
        )
        p_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content p")
        last_paragraph = p_elements[-1]
        driver.execute_script(
            f"arguments[0].textContent = '{description}'",
            last_paragraph,
        )
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Add room')]")
            )
        ).click()

    def create_tile(self, tile_name, tile_description):
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[@class='form-overlay']")
            )
        )
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal fade"))
        )
        # Wait for the modal-backdrop fade to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        # Add an additional wait to make sure the modal fade element is no longer obscuring the home icon
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "glyphicon-plus"))
        ).click()
        # Finding the element by the <small> element works, but when I want to find it by picking the first li of the list it says it has to scroll it into view... weird.
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//small[contains(text(), 'New tile can contain description, tasks, comments and uploaded files')]",
                )
            )
        ).click()
        # Input Tile Name
        self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input#data-name.form-control")
            )
        ).send_keys(tile_name)
        p_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content p")
        last_paragraph = p_elements[-1]
        driver.execute_script(
            f"arguments[0].textContent = '{tile_description}'",
            last_paragraph,
        )
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add tile')]").click()

    def add_file(self, file_path):
        self.wait.until(
            EC.invisibility_of_element_located((By.XPATH, "//div[@class='form-overlay']"))
        )
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal fade"))
        )
        # Wait for the modal-backdrop fade to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        print("modal backdrop fade disappeared successfully")
        # Wait for the files toggle to be clickable
        files_toggle = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.files-toggle"))
        )
        print("files toggle is clickable")

        # Click the files toggle using JavaScript
        self.driver.execute_script("arguments[0].click();", files_toggle)
        print("files toggle clicked")

        # Click on "Add files"
        add_files_link = self.driver.find_element(By.LINK_TEXT, "Add files")
        self.driver.execute_script("arguments[0].click();", add_files_link)
        print("files added")

        # Find the input element for file upload
        file_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        print("input element for file upload found")

        # Send the file path to the input element
        file_input.send_keys(file_path)
        print("file path sent to the input element")

        # Click on OK
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
        ).click()

        # Navigate back (assuming you want to go back after adding the file)
        self.driver.back()
        print("Successfully navigated back")

    def check_element_presence(self, xpath):
        """Check if an element with the given xpath is present on the page."""

        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            print("Found expected results")
        except TimeoutException:
            print("Didn't find expected results")

    def click_button(self, text):
        """Click on a button with the given text."""
        driver.find_element(
            By.XPATH, f"//button[contains(@class, 'chip') and text()='{text}']"
        ).click()

    def verify_everything(self):
        driver.find_element(By.ID, "search-rooms-input").send_keys("Private")
        print(
            "Checking if 'private rooms' shows up when looking up 'private' in the searchbar..."
        )
        self.check_element_presence(
            "//div[@class='search-items__item-title' and text()='Private Rooms']"
        )

        print("Checking if the h3 with 'private' marked and text ' Rooms' shows up...")
        self.check_element_presence("//h3[mark='Private' and text()=' Rooms']")

        print(
            "Checking if a div of class creation-details with a paragraph with Hoshito's name and text 'Created by' shows up..."
        )
        self.check_element_presence(
            "//div[@class='creation-details']/p[strong='Hoshito Shimakawa' and contains(text(),'Created by')]"
        )

        # Disabling rooms
        self.click_button("Rooms")

        print("Disabling rooms category and seeing if the right h4 shows up")
        self.check_element_presence("//h4[text()='No results found']")

        # Disabling all the categories, but the first two (rooms already disables, tasks has to be left on)
        print("Checking if test task shows up after typing in 'Test'...")
        category_buttons = driver.find_elements(By.XPATH, "//button[@class='chip']")[1:]
        for button in category_buttons:
            button.click()

        driver.find_element(By.ID, "search-rooms-input").clear()
        driver.find_element(By.ID, "search-rooms-input").send_keys("Test")
        print("Checking if tile shows up after typing in the name 'い')...")
        self.check_element_presence(
            "//div[@class='search-items__item-title' and text()='Test task']"
        )
        driver.find_element(By.ID, "search-rooms-input").clear()
        driver.find_element(By.ID, "search-rooms-input").send_keys("い")
        category_buttons = driver.find_elements(By.XPATH, "//button[@class='chip']")
        for button in category_buttons:
            button.click()
        self.click_button("Tiles")
        self.check_element_presence(
            "//div[@class='search-items__item-title' and text()='い']"
        )
        print("Checking if it shows the appropriate parent room")
        self.check_element_presence("//small[text()='TEST dpt ']")
        print("Checking if Filip Pacamaj shows up after typing in 'Filip'...")
        self.click_button("People")
        driver.find_element(By.ID, "search-rooms-input").clear()
        driver.find_element(By.ID, "search-rooms-input").send_keys("Filip")
        self.check_element_presence(
            "//div[@class='search-items__item-title' and text()='Filip Pacamaj']"
        )
        """
        print("Checking if the creation date lines up...")
        self.check_element_presence(
            "//p[strong='Created: ' and text()='August 6th 2018, 8:37:10 am']"
        )
        time.sleep(5)
        """
        print("Checking if the file shows up after typing in 'TheWonders'")
        self.click_button("Files")
        driver.find_element(By.ID, "search-rooms-input").clear()
        driver.find_element(By.ID, "search-rooms-input").send_keys("TheWonders")
        self.check_element_presence(
            "//div[@class='search-items__item-title search-items__item-title--is-file' and text()='TheWondersOfNature.txt']"
        )


bot = Searchbar_test()
if __name__ == "__main__":
    try:
        bot.login()
        bot.go_into_TESTdpt()
        bot.create_tile("い", "いいいいいいいいいいいいいい")
        print("Creating a task...")
        bot.create_task("Test task")
        print("Created test task")
        bot.add_file(file_path)
        print("Added file")
        bot.verify_everything()
        print("Everything has been verified")
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
