import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import os
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.common.exceptions import NoAlertPresentException
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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


class Task_tests:
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
        self.room_name = "Test room"
        self.tile_name = "Kenja Tile"
        self.task_name = "Kenja task"
        self.comment_content = "Great job!"
        self.progress_value = "50%"
        self.subtask_name = "Kenja Subtask"
        os.environ["PATH"] += self.webdriver_path
        super(Task_tests, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def __enter__(self):
        return self

    def login(self):
        self.driver.get("https://kenja.rooms3.dvl/#")
        self.driver.execute_script("document.body.style.zoom='100%'")
        self.driver.maximize_window()

        # Enter email address and password
        self.driver.find_element(By.ID, "login-input-email").send_keys(
            self.email_address
        )
        self.driver.find_element(By.ID, "login-input-password").send_keys(self.password)

        # Click login button
        self.driver.find_element(By.CSS_SELECTOR, ".btn-block").click()

        # Wait for login to complete
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".header-bottom-menu-add > .header-bottom-menu-item")
            )
        )

    def create_room(self):
        # Find "create room" button

        driver.find_element(
            By.CSS_SELECTOR, ".header-bottom-menu-add > .header-bottom-menu-item"
        ).click()
        # Click create room
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".modal-footer > .btn:nth-child(4)")
            )
        )
        element.click()
        print("Trying to create a room...")
        # Try to input empty name
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[@class='field-error']")
                )
            )
            print("Room naming works properly")
        except:
            print("'Room name may not be empty' - not showing up")
        # Set actual name
        driver.find_element(By.ID, "data-name").send_keys(self.room_name)
        driver.find_element(
            By.CSS_SELECTOR, ".modal-footer > .btn:nth-child(4)"
        ).click()
        print("Created room")
        # Find the header with the room name on it
        time.sleep(1)  # TO DO: Change that... this is a very lazy fix
        header_text = driver.find_element(By.CLASS_NAME, "header-bottom-room-name")
        text = header_text.text
        if text == self.room_name:
            print("The room title shows up in the corner as expected")
        else:
            print(
                f"The room title doesn't show up in the corner. {text} shows up instead."
            )

    def create_tile(self):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal fade")))
        # Wait for the modal-backdrop fade to disappear
        wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        # Add an additional wait to make sure the modal fade element is no longer obscuring the home icon
        wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "glyphicon-plus"))
        ).click()

        # Finding the element by the <small> element works, but when I want to find it by picking the first li of the list it says it has to scroll it into view... weird.
        driver.find_element(
            By.XPATH,
            "//small[contains(text(), 'New tile can contain description, tasks, comments and uploaded files')]",
        ).click()

        # Try to save tile
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Add tile']"))
        ).click()

        # See if the error shows up
        try:
            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[@class='field-error']")
                )
            )
            print("The error for empty title shows up appropriately for tiles")
        except:
            print("The error message for empty title doesn't show up for tiles")
        # Input Tile Name
        driver.find_element(By.CSS_SELECTOR, "input#data-name.form-control").send_keys(
            self.tile_name
        )
        # Pin tile
        driver.find_element(By.ID, "data-important").click()
        driver.find_element(By.XPATH, "//button[text()='Add tile']").click()

    def create_task(self):
        # Wait for the modal-backdrop fade to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        # Click on tasks tab
        driver.find_element(By.CSS_SELECTOR, "div[data-toggle='tasks']").click()
        # Click on "Add new task"
        driver.find_element(By.LINK_TEXT, "Add new task").click()
        # Set the name
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "data-name"))
        ).send_keys(self.task_name)
        # Click on the asignee input

        driver.find_element(
            By.CSS_SELECTOR, "input[type='text'][value='Assignee not defined yet.']"
        ).click()
        # Click on the first result
        driver.find_element(By.CSS_SELECTOR, "li[data-option-array-index='0']").click()
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
        # Get the current date and time
        now = datetime.now()
        # Format the date and time as a string
        task_date = now.strftime("%Y-%m-%d %H:%M")
        self.task_date = task_date
        return task_date

    # Checks if the tile that shows up matches up to all the info
    def verify_tile(self):
        driver.implicitly_wait(5)
        try:
            driver.find_element(By.XPATH, f"//span[text()='{self.task_name}']")
            print("Tile shows up and is named properly")
        except NoSuchElementException:
            print("Tile doesn't show up or the name doesn't display properly")
        try:
            driver.find_element(By.XPATH, f"//span[text()='{self.task_name}']")
            print("Task shows up and is named properly")
        except NoSuchElementException:
            print("Task doesn't show up or the name doesn't display properly")
        print(
            "WARNING, ROOMS TIME AND YOUR COMPUTERS TIME WOULD HAVE TO BE IDENTICAL FOR THIS TO WORK SO THIS IS VERY ERROR PRONE"
        )
        try:
            driver.find_element(
                By.XPATH,
                f"//span[@class='pull-right task-end-date' and text()='{self.task_name}']",
            )
            print(
                f"There is at least one span element with the task creation date '{self.task_date}' on the page"
            )
        except NoSuchElementException:
            print(
                f"There is no span element with the task creation date '{self.task_date}' on the page"
            )

        try:
            driver.find_element(By.CLASS_NAME, "acknowledge-do")
            print("Acknowledge btn shows up")
            driver.find_element(By.CLASS_NAME, "approve-do")
            print("Approve btn shows up")
            driver.find_element(By.CLASS_NAME, "review-do")
            print("Review btn shows up")
        except NoSuchElementException:
            print(
                "At least one of the Acknowledge/Approve/Review buttons doesn't show up"
            )

    def write_comment(self):
        driver.find_element(By.CSS_SELECTOR, "[data-toggle='comments']").click()
        driver.implicitly_wait(3)
        driver.find_element(By.CLASS_NAME, "emoji-wysiwyg-editor").send_keys(
            self.comment_content
        )
        # Add an emoticon
        driver.find_element(By.ID, "dropEmoticons").click()
        driver.find_element(By.XPATH, "//img[@alt='Love it']").click()
        driver.find_element(By.CLASS_NAME, "btn-primary").click()

    def check_side_bar(self):
        driver.find_element(By.CLASS_NAME, "task-content").click()
        # Progress check
        progress_input = driver.find_element(By.CLASS_NAME, "task-progress-value")
        progress_input.clear()
        progress_input.send_keys("50")
        progress_input.send_keys(Keys.ENTER)
        try:
            element = driver.find_element(By.CLASS_NAME, "in-progress-bar-background")
            text = element.get_attribute("textContent")
            if text == self.progress_value:
                print("Progress shows appropriate value")
            else:
                print("Progress shows wrong value or doesn't show up at all")
        except NoSuchElementException:
            print("Couldn't find progress bar")
        # This checks the properties listed in the side tab that pops up when the task content is clicked
        try:
            element = driver.find_element(By.XPATH, "//a[@title='Go to Tile']")
            if element.text == self.tile_name:
                print("The text of the 'Tile:' property is appropriate")
            else:
                print("The text of the 'Tile:' property isn't appropriate")
        except NoSuchElementException:
            print("Couldn't find 'Tile:' property")
        try:
            element = driver.find_element(By.XPATH, "//a[@title='Go to Room']")
            if element.text == self.room_name:
                print("The text of the 'Room:' property is appropriate")
            else:
                print("The text of the 'Room:' property isn't appropriate")
        except NoSuchElementException:
            print("Couldn't find 'Room:' property")

    def send_email_reminder(self):
        driver.find_element(By.LINK_TEXT, "Send reminder").click()
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            print("No alert present")
        print("Clicked the 'Send reminder' button")
        try:
            driver.find_element(By.XPATH, "//span[text()='Task reminder sent']")
            print("Task reminder notification shows up")
        except NoSuchElementException:
            print("Task reminder notification doesn't show up")

    def add_subtask(self):
        print("Creating subtask...")
        driver.find_element(By.LINK_TEXT, "Add new subtask").click()
        driver.find_element(By.CSS_SELECTOR, "input#data-name.form-control").send_keys(
            self.subtask_name
        )
        driver.find_element(By.XPATH, "//button[text()='Add task']").click()
        # Check if subtask is showing up
        try:
            driver.find_element(By.XPATH, f"//span[text()='{self.subtask_name}']")
            print("Subtask present on page")
        except NoSuchElementException:
            print(
                "Can't find the subtask on page or the subtask's name isn't displaying properly"
            )

    def delete_subtask(self):
        print("Now it's time to delete the subtask...")
        wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds
        element = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[text()='{self.subtask_name}']")
            )
        )
        element.click()
        driver.find_element(By.LINK_TEXT, "Delete").click()
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            print("The alert for deletion wasn't located...")
        print("Subtask deleted")
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(
                EC.invisibility_of_element_located(
                    (By.XPATH, f"//span[text()='{self.subtask_name}']")
                )
            )
            print("Subtask was deleted and doesn't appear on the page as expected")
        except TimeoutException:
            print(
                "Subtask seems to still show up on the page, even though it was deleted"
            )

    def go_to_dashboard(self):
        driver.find_element(By.CLASS_NAME, "glyphicon-home").click()

    def check_if_task_shows_up(self):
        try:
            driver.find_element(
                By.XPATH, f"//div[contains(text(), '{self.task_name}')]"
            )
            print("Task shows up in dashboard")
        except NoSuchElementException:
            print("Task doesn't show up in dashboard")

    def check_if_room_shows_up(self):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//a[@title='{self.room_name}']")
                )
            )
            print(f"{self.room_name} shows up in the dashboard")
        except NoSuchElementException:
            print(f"{self.room_name} doesn't show up in the dashboard")

    def check_rooms_tab(self):
        # Click rooms tab
        driver.find_element(By.CSS_SELECTOR, "a[title='Rooms']").click()
        print("Opened rooms tab")
        # Check if the room exists
        try:
            driver.find_element(
                By.XPATH,
                f"//div[@class='header-title data-open-room' and text()='{self.room_name}']",
            )
            print(f"{self.room_name} shows up in the rooms tab")
        except NoSuchElementException:
            print(f"{self.room_name} doesn't show up in the rooms tab")

    def check_tasks_tab(self):
        print("Time to check out the taks tab...")
        driver.find_element(By.CSS_SELECTOR, "a[title='Tasks']").click()
        # You have to click away on something or else it can't detect the task
        driver.find_element(By.CLASS_NAME, "task-details").click()
        wait = WebDriverWait(driver, 10)
        try:
            # wait until the element is present on the website
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//span[@class='name' and text()='{self.task_name}']")
                )
            )
            print("Task shows up in Task tab")
        except TimeoutException:
            print("Task doesn't show up in the task tab")

    def delete_room(self):
        print("Almost done. Now onto deleting the room")
        driver.implicitly_wait(15)
        driver.find_element(By.LINK_TEXT, f"{self.room_name}").click()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "kenjaicon-options").click()

        driver.find_element(
            By.CSS_SELECTOR, "li:nth-child(10) > .header-menu-icon-delete"
        ).click()
        # Accept popup
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            print("No alert present for room deletion")
        print("Room has been deleted...")
