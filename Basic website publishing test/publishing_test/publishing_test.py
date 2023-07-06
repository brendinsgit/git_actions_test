import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import os
from selenium.webdriver.support import expected_conditions as EC
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


class Publishing_test:
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
        os.environ["PATH"] += self.webdriver_path
        super(Publishing_test, self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def __enter__(self):
        return self

    def login(self):
        self.driver.get("https://kenja.rooms3.dvl/#")
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
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".modal-footer > .btn:nth-child(4)")
            )
        )
        print("Trying to create a room...")
        driver.find_element(By.ID, "data-name").send_keys("Publishing rooms")
        driver.find_element(
            By.CSS_SELECTOR, ".modal-footer > .btn:nth-child(4)"
        ).click()
        print("Created room")

    def create_first_tile(self):
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
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//small[contains(text(), 'New tile can contain description, tasks, comments and uploaded files')]",
                )
            )
        ).click()

        # Input Tile Name
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input#data-name.form-control")
            )
        ).send_keys("First Tile")

        # In order to put in a description, we have to use JS scripts, because the description isn't an input or a text-area
        lorem_ipsum_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, velit et tincidunt tincidunt, nisl velit bibendum nulla, vel lacinia orci magna vel justo. Sed euismod, felis non ultricies tincidunt, justo massa tincidunt velit, vel lacinia orci magna vel justo."
        driver.execute_script(
            f"document.querySelector('div.ck-content > p').textContent = '{lorem_ipsum_text}'"
        )
        # Try to save tile
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Add tile']"))
        ).click()

    def create_second_tile(self):
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
        # Input Tile Name
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input#data-name.form-control")
            )
        ).send_keys("Second Tile")
        # In order to put in a description, we have to use JS scripts, because the description isn't an input or a text-area
        lorem_ipsum_text = "Vivamus auctor, velit eu luctus tincidunt, nisl velit bibendum nulla, vel lacinia orci magna vel justo. Nullam euismod, velit et tincidunt tincidunt, nisl velit bibendum nulla, vel lacinia orci magna vel justo. Sed euismod, felis non ultricies tincidunt, justo massa tincidunt velit, vel lacinia orci magna vel justo. Sed euismod, felis non ultricies tincidunt, justo massa tincidunt velit, vel lacinia orci magna vel justo"
        driver.execute_script(
            f"document.querySelector('div.ck-content > p').textContent = '{lorem_ipsum_text}'"
        )
        # Try to save tile
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Add tile']"))
        ).click()

    def add_file_to_tile(self):
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal fade"))
        )
        # Wait for the modal-backdrop fade to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        driver.find_element(By.CLASS_NAME, "files-toggle").click()
        driver.find_element(By.CLASS_NAME, "add-file").click()
        driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys("")

        driver.find_element(By.CLASS_NAME, "btn-primary").click()

    def add_comment(self):
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal fade"))
        )
        # Wait for the modal-backdrop fade to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        driver.find_element(By.CLASS_NAME, "comments-toggle").click()
        driver.execute_script(
            f"document.querySelector('div.emoji-wysiwyg-editor').textContent = 'WOOOOOOW'"
        )
        driver.find_element(By.XPATH, "//button[text()='Add']").click()

    def publish_room(self):
        wait = WebDriverWait(driver, 10)
        # Wait for the modal-backdrop fade to disappear
        wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        print("Time to publish the room...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "glyphicon-globe"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Publish as a new site']")
            )
        ).click()
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal fade")))
        publish_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Publish']"))
        )
        publish_button.click()

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[@class="list-group-item-text data-hide-pending"]/a')
            )
        )
        href = element.get_attribute("href")
        driver.get(href)
        print(href)

    def verify_published_page(self):
        print("Checking if all elements are showing...")
        wait = WebDriverWait(driver, 10)
        elements = [
            ("Room title", "h1", "Publishing rooms"),
            ("First Tile", "h2", "First Tile"),
            ("Second Tile", "h2", "Second Tile"),
            (
                "Tile 1 description",
                "p",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, velit et tincidunt tincidunt, nisl velit bibendum nulla, vel lacinia orci magna vel justo. Sed euismod, felis non ultricies tincidunt, justo massa tincidunt velit, vel lacinia orci magna vel justo.",
            ),
            (
                "Tile 2 description",
                "p",
                "Vivamus auctor, velit eu luctus tincidunt, nisl velit bibendum nulla, vel lacinia orci magna vel justo. Nullam euismod, velit et tincidunt tincidunt, nisl velit bibendum nulla, vel lacinia orci magna vel justo. Sed euismod, felis non ultricies tincidunt, justo massa tincidunt velit, vel lacinia orci magna vel justo. Sed euismod, felis non ultricies tincidunt, justo massa tincidunt velit, vel lacinia orci magna vel justo",
            ),
        ]
        for element in elements:
            try:
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"//{element[1]}[text()='{element[2]}']")
                    )
                )
                print(f"Found {element[0]}")
            except (NoSuchElementException, TimeoutException):
                print(
                    f"Couldn't find {element[0]}, looked for an {element[1]} of '{element[2]}'"
                )

    def verify_search(self):
        print("Checking the search...")
        driver.find_element(By.CLASS_NAME, "form-control").send_keys("Tile")
        driver.find_element(By.CLASS_NAME, "btn-default").click()
        try:
            result_statistics = driver.find_element(
                By.XPATH, '//div[@class="search-statistics"]/strong'
            )
            text = result_statistics.text
            if text == "2":
                print("The search statistic works properly ")
            else:
                print(
                    f"The search statistic shows  '{text}', instead of 2 as it was expected"
                )
        except Exception as e:
            print(f"An error occurred: {e}")
        tiles = ["First", "Second"]
        for tile in tiles:
            try:
                h4 = driver.find_element(By.XPATH, f"//h4[contains(text(), '{tile}')]")
                h4.find_element(
                    By.XPATH, ".//span[@class='highlight' and contains(text(), 'Tile')]"
                )
                print(f"Found the {tile} tile")
            except NoSuchElementException:
                print(f"Couldn't find the {tile} tile")
        driver.find_element(By.CLASS_NAME, "form-control").send_keys("1234")
        driver.find_element(By.CLASS_NAME, "btn-default").click()
        print("Checking what happens when 1234 is searched")
        for tile in tiles:
            try:
                h4 = driver.find_element(By.XPATH, f"//h4[contains(text(), '{tile}')]")
                h4.find_element(
                    By.XPATH, ".//span[@class='highlight' and contains(text(), 'Tile')]"
                )
                raise Exception(f"Found the {tile} tile, when it shouldn't show up")
            except NoSuchElementException:
                print(f"{tile} didn't show up, that's good ")
        print("Checking what happens when nothing is searched...")
        driver.find_element(By.CLASS_NAME, "form-control").clear()
        driver.find_element(By.CLASS_NAME, "btn-default").click()
        try:
            driver.find_element(
                By.XPATH,
                "//div[@class='search-statistics' and contains(text(), 'No results found')]",
            )
            print("'No results found' shows up as expected")
        except NoSuchElementException:
            print("'No results found' doesn't seem to show up")
        driver.find_element(By.LINK_TEXT, "Home").click()
