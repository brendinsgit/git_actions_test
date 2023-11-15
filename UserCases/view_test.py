import os
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
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)


# browser = input("Enter your preferred browser (Firefox, Edge or Chrome): ")
webdriver_path = ChromeDriverManager().install()
email_address = "max.gapa+automation_tests@kenja.com"
password = "automation_testing1234"
img_path = os.path.abspath("./TestFiles/doggo.png")
os.environ["PATH"] += os.pathsep + webdriver_path


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


chrome_options = Options()
options = [
    "--headless",
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


class View_test:
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
        self.teardown = teardown
        self.image_path = img_path
        self.wait = WebDriverWait(self.driver, 30)
        os.environ["PATH"] += self.webdriver_path
        super(View_test, self).__init__()

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

    def create_room(self):
        # Go into TEST dpt
        self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Private Rooms"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'TEST dpt')]"))
        ).click()

        # Click on the plus icon next to "Add"
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "glyphicon-plus"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Add sub room')]")
            )
        ).click()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "data[name]"))).send_keys(
            "View test room"
        )
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Add room')]")
            )
        ).click()

    """

    def create_room(self):
        # Click on the plus icon next to "Add"
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "glyphicon-plus"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Add room')]"))
        ).click()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "data[name]"))).send_keys(
            "View test room"
        )
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Add room')]")
            )
        ).click()
"""

    def create_tile(self, tile_number):
        # Wait for the modal-backdrop fade to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        element = self.wait.until(
            lambda driver: EC.visibility_of_element_located(
                (By.CLASS_NAME, "glyphicon-plus")
            )(driver)
            or EC.element_to_be_clickable((By.CLASS_NAME, "glyphicon-plus"))(driver)
        )
        element.click()

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
        ).send_keys(f"View test tile {tile_number}")

        driver.find_element(By.XPATH, "//button[contains(text(), 'Add tile')]").click()

    def add_file(self):
        # Make sure the view is set to 3 columns
        driver.find_element(By.XPATH, "//div[@title='Views']").click()
        driver.find_element(
            By.XPATH, "//*[text()='Display content of this room in 3 columns']"
        ).click()

        fileDropDowns = driver.find_elements(By.CSS_SELECTOR, "div.files-toggle")
        for dropdown in fileDropDowns:
            dropdown.click()

        addFileBtns = driver.find_elements(By.LINK_TEXT, "Add files")
        addFileBtns[0].click()

        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(
            f"{self.image_path}"
        )
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
        ).click()

    def add_task(self):
        # Wait for the modal-backdrop fade to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        # Click on tasks tab
        driver.find_element(By.CSS_SELECTOR, "div[data-toggle='tasks']").click()
        # Click on "Add new task"
        driver.find_element(By.LINK_TEXT, "Add new task").click()
        # Set the name
        self.wait.until(EC.element_to_be_clickable((By.ID, "data-name"))).send_keys(
            "Kenja Task"
        )
        driver.find_element(By.XPATH, "//button[text()='Add task']").click()

    def add_comment(self):
        # Wait for the modal-backdrop fade to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )

        # Click on comments tab
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-toggle='comments']"))
        ).click()

        js = "document.querySelector('.emoji-wysiwyg-editor').textContent = 'Basic comment'"
        driver.execute_script(js)
        # Add an emoticon. Else the js that was put in earlier will be ignored and it will act as if the field was empty
        driver.find_element(By.CLASS_NAME, "emo-button").click()
        driver.find_element(By.XPATH, "//a[@data-emoticon='[feeling good]']").click()

        driver.find_element(By.XPATH, "//button[@name='add' and text()='Add']").click()

    def add_subroom(self):
        # Wait for the modal-backdrop fade to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        # Click on the plus icon next to "Add"
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "glyphicon-plus"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Add sub room')]")
            )
        ).click()
        self.wait.until(EC.element_to_be_clickable((By.NAME, "data[name]"))).send_keys(
            "View test subroom"
        )
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Add room')]")
            )
        ).click()

        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ui-empty-title"))
        )
        driver.back()

    def switch_to_two_column(self):
        driver.find_element(By.XPATH, "//div[@title='Views']").click()
        driver.find_element(
            By.XPATH, "//*[text()='Display content of this room in 2 columns']"
        ).click()
        print("Time to check if everything shows up in 2 column view")

    def verify_everything(self):
        def check_element(driver, by, value, description):
            driver.implicitly_wait(15)
            try:
                driver.find_element(by, value)
                print(f"{description} found!")
            except NoSuchElementException:
                print(f"{description} not found.")

        check_element(
            driver,
            By.XPATH,
            "//span[text()='View test subroom']",
            "Room title 'View test Subroom'",
        )
        for i in range(4):
            check_element(
                driver,
                By.XPATH,
                f"//span[text()='View test tile {i}']",
                f"Room title 'View test tile {i}'",
            )
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@class='name' and text()='Kenja Task']")
            )
        )

        check_element(
            driver,
            By.XPATH,
            f"//span[@class='name' and text()='Kenja Task']",
            f"Kenja Task",
        )
        check_element(
            driver, By.LINK_TEXT, "doggo.png", "The doggo file by it's link text"
        )
        check_element(
            driver,
            By.XPATH,
            "//img[@src='/emoticons/emo_02.png']",
            "Basic comment by it's text and the emoticon",
        )

    def switch_to_one_column(self):
        driver.find_element(By.XPATH, "//div[@title='Views']").click()
        driver.find_element(
            By.XPATH, "//*[text()='Display content of this room as list']"
        ).click()
        print("Time to check if everything shows up in 1 column view")

    def switch_to_even_tiles(self):
        driver.find_element(By.XPATH, "//div[@title='Views']").click()
        driver.find_element(
            By.XPATH, "//*[text()='Display content of this room with even tile size']"
        ).click()
        print("Time to check if everything shows up in even tiles view")

    def switch_to_mini_tiles(self):
        driver.find_element(By.XPATH, "//div[@title='Views']").click()
        driver.find_element(
            By.XPATH, "//*[text()='Display content of this room as tiles']"
        ).click()
        print("Time to check if everything shows up as tiles")

    def switch_to_table_view(self):
        driver.find_element(By.XPATH, "//div[@title='Views']").click()
        driver.find_element(
            By.XPATH, "//*[text()='Display content of this room as table']"
        ).click()
        print("Time to check if everything shows up in table view")

    def verify_everything_mini(self):
        def check_element(driver, by, value, description):
            try:
                driver.find_element(by, value)
                print(f"{description} found!")
            except NoSuchElementException:
                print(f"{description} not found.")

        check_element(
            driver,
            By.XPATH,
            "//span[text()='View test subroom']",
            "Span with text 'View Test subroomm'",
        )
        for i in range(4):
            check_element(
                driver,
                By.XPATH,
                f"//span[text()='View test tile {i}']",
                f"Room title 'View test tile {i}'",
            )
        check_element(
            driver,
            By.XPATH,
            "//span[@class='count' and text()='1']",
            "Span with class count and text content 1",
        )

    def verify_everything_table(self):
        def check_element(driver, by, value, description):
            try:
                driver.find_element(by, value)
                print(f"{description} found!")
            except NoSuchElementException:
                print(f"{description} not found.")

        check_element(
            driver,
            By.LINK_TEXT,
            "View test subroom",
            "<a> with link test 'View test subroom'",
        )

        for i in range(4):
            check_element(
                driver,
                By.XPATH,
                f"//td[normalize-space(text())='View test tile {i}']",
                f"<td> with text content 'View test tile {i}'",
            )
        check_element(
            driver,
            By.XPATH,
            f"//td[normalize-space(text())='1']",
            f"<td> with text content '1'",
        )
        print(
            "In order for this check to work the dates on your computer and rooms have to line up"
        )
        current_date = datetime.now().strftime("%Y-%m-%d")
        check_element(
            driver,
            By.XPATH,
            f"//td[normalize-space(text())='{current_date}']",
            f"<td> with text content '{current_date}'",
        )

    def verify_everything_even(self):
        def check_element(driver, by, value, description):
            try:
                driver.find_element(by, value)
                print(f"{description} found!")
            except NoSuchElementException:
                print(f"{description} not found.")

        check_element(
            driver,
            By.XPATH,
            "//span[text()='View test subroom']",
            "Room title 'View test Subroom'",
        )
        for i in range(4):
            check_element(
                driver,
                By.XPATH,
                f"//span[text()='View test tile {i}']",
                f"Room title 'View test tile {i}'",
            )
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@class='name' and text()='Kenja Task']")
            )
        )

        check_element(
            driver,
            By.XPATH,
            f"//span[@class='name' and text()='Kenja Task']",
            f"Kenja Task",
        )
        driver.find_element(By.CLASS_NAME, "tile-size-control").click()

        check_element(
            driver, By.LINK_TEXT, "doggo.png", "The doggo file by it's link text"
        )
        check_element(
            driver,
            By.XPATH,
            "//img[@src='/emoticons/emo_02.png']",
            "Basic comment by it's text and the emoticon",
        )


bot = View_test()
if __name__ == "__main__":
    try:
        bot.login()
        bot.create_room()
        for i in range(4):
            bot.create_tile(i)
        bot.add_file()
        bot.add_task()
        bot.add_comment()
        bot.add_subroom()
        bot.switch_to_two_column()
        bot.verify_everything()
        bot.switch_to_one_column()
        bot.verify_everything()
        bot.switch_to_even_tiles()
        bot.verify_everything_even()
        bot.switch_to_mini_tiles()
        bot.verify_everything_mini()  # Alternative version for mini tiles view
        bot.switch_to_table_view()
        bot.verify_everything_table()

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
