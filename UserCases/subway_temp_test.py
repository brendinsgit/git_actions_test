import os
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)
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


webdriver_path = input("Enter the path to your Chrome webdriver: ")
email_address = input("Please provide an email that can be used to log in: ")
password = input("Please provide a password that can be used to log in: ")
file_path = input(
    "Please provide the absolute path to the file (More info in QA Line doc): "
)
os.environ["PATH"] += os.pathsep + webdriver_path

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options)


class Subway_template_test:
    def __init__(
        self,
        webdriver_path=webdriver_path,
        email_address=email_address,
        password=password,
        teardown=False,
    ):
        self.driver = driver
        self.webdriver_path = webdriver_path
        self.email_address = email_address
        self.password = password
        self.teardown = teardown
        self.file_path = file_path
        self.wait = WebDriverWait(self.driver, 30)
        os.environ["PATH"] += self.webdriver_path
        super(Subway_template_test, self).__init__()

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
        self.driver.find_element(By.ID, "login-input-email").send_keys(email_address)
        self.driver.find_element(By.ID, "login-input-password").send_keys(password)

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

    def add_file(self):
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
        time.sleep(1)
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.files-toggle"))
        ).click()
        driver.find_element(By.LINK_TEXT, "Add files").click()
        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(
            f"{self.file_path}"
        )
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
        ).click()
        driver.back()

    def create_forbidden_tile(self, tile_name, tile_description):
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
        driver.find_element(By.ID, "data-publish_locked").click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add tile')]").click()

    def go_to_subway_theme_test(self):
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
        driver.find_element(
            By.XPATH,
            "//span[@class='breadcrumb-label' and text()='Subway theme test']",
        ).click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Subway theme test')]")
            )
        )
        time.sleep(5)

    def open_website_publishing(self):
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
        print("Time to publish the room...")
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "glyphicon-globe"))
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Publish as a new site']")
            )
        ).click()
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal fade"))
        )

    def edit_appearance_and_publish(self):
        self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Appearance"))
        ).click()
        Select(driver.find_element(By.ID, "data-template")).select_by_value("subway")

        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Publish']"))
        ).click()
        element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//p[@class="list-group-item-text data-hide-pending"]/a')
            )
        )
        href = element.get_attribute("href")
        driver.get(href)

    def verify_published_homepage(self):
        print("Checking if all elements are showing...")

        elements = [
            ("Subway theme test tile title", "h1", "Subway theme test"),
            (
                "The Benefits of Volunteering tile title",
                "h3",
                "The Benefits of Volunteering",
            ),
            (
                "Tile Subway theme test tile description",
                "div",
                "As the world continues to face the challenges of climate change, the need for sustainable energy sources has never been more pressing.",
            ),
            (
                "The Benefits of Learning a New Language tile title",
                "h3",
                "The Benefits of Learning a New Language",
            ),
            (
                "Tile 1 description",
                "p",
                "Volunteering is an amazing way to give back to our communities and make a positive impact in the world. It allows us to help others, learn new skills, and connect with like-minded individuals.",
            ),
            (
                "Tile 2 description",
                "p",
                "Learning a new language is an amazing way to expand our horizons and connect with other cultures. It allows us to communicate with people from different parts of the world, and opens up new opportunities for travel, work, and personal growth.",
            ),
            (
                "Top nav creative expression link",
                "a",
                "The Benefits of Creative Expression",
            ),
            (
                "Top nav travel benefits link",
                "a",
                "The Benefits of Travel",
            ),
            (
                "Travel benefits subroom name",
                "div",
                "The Benefits of Travel",
            ),
            (
                "Creative expression subroom name",
                "div",
                "The Benefits of Creative Expression",
            ),
        ]
        self.verify_elements(elements)

    def verify_benefits_subroom(self):
        driver.find_element(By.LINK_TEXT, "The Benefits of Travel").click()
        elements = [
            ("Benefits of travel h1", "h1", "The Benefits of Travel"),
            (
                "The Importance of Regular Exercise title h3",
                "h3",
                "The Importance of Regular Exercise",
            ),
            (
                "Benefits of travel div description",
                "div",
                "Travel is an amazing way to broaden our horizons and experience new cultures. It allows us to step outside of our comfort zones and see the world from a different perspective.",
            ),
            (
                "The Benefits of Mindfulness Meditation h2 title",
                "h3",
                "The Benefits of Mindfulness Meditation",
            ),
            (
                "TheWondersOfNature tile title",
                "h3",
                "TheWondersOfNature",
            ),
            (
                "The Importance of Regular Exercise description",
                "p",
                "Regular exercise is essential for maintaining good health and preventing chronic diseases. It can improve cardiovascular health, strengthen bones and muscles, and boost mental health.",
            ),
            (
                "Mindfullness meditation description",
                "p",
                "Mindfulness meditation is a practice that involves focusing your attention on the present moment, without judgment. It has been shown to have numerous benefits for both physical and mental health.",
            ),
            (
                "TheWondersOfNature file title",
                "a",
                "TheWondersOfNature.txt",
            ),
        ]
        self.verify_elements(elements)

    def verify_elements(self, elements):
        for element in elements:
            if len(element) == 5:
                xpath = f"//{element[3]}[@class='{element[4]}']//{element[1]}[normalize-space(.)='{element[2]}']"
            else:
                xpath = f"//{element[1]}[normalize-space(.)='{element[2]}']"

            try:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                print(f"Found {element[0]}")
            except (NoSuchElementException, TimeoutException):
                print(
                    f"Couldn't find {element[0]}, looked for an {element[1]} of '{element[2]}'"
                )

    def verify_creative_expression_subroom(self):
        driver.find_element(By.LINK_TEXT, "The Benefits of Creative Expression").click()
        elements = [
            (
                "The Benefits of Creative Expression h1",
                "h1",
                "The Benefits of Creative Expression",
            ),
            (
                "The Benefits of Creative Expression div description",
                "div",
                "Creative expression is an amazing way to explore our inner selves and share our unique perspectives with the world. Whether it’s through art, music, writing, or other forms of creativity, expressing ourselves creatively can have numerous benefits for our mental health and well-being.",
            ),
        ]
        self.verify_elements(elements)

    def verify_mindful_eating_subroom(self):
        driver.find_element(By.LINK_TEXT, "The Benefits of Mindful Eating").click()
        elements = [
            (
                "The Benefits of Mindful Eating h1",
                "h1",
                "The Benefits of Mindful Eating",
            ),
            (
                "The Benefits of Mindful Eating div description",
                "div",
                "Mindful eating is the practice of paying attention to our food and the experience of eating. It involves being present in the moment, savoring the flavors and textures of our food, and listening to our body’s hunger and fullness cues.",
            ),
            (
                "The Benefits of Positive Thinking",
                "h3",
                "The Benefits of Positive Thinking",
            ),
            (
                "The Benefits of Positive Thinking description",
                "p",
                "Positive thinking is the practice of focusing on the good in any situation and maintaining a positive outlook on life. It has been shown to have numerous benefits for our mental and physical health.",
            ),
        ]
        try:
            self.wait.until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//h1[normalize-space(.)='Forbidden tile']")
                )
            )
            print("Forbidden tile not showing up - that's a good thing")
        except TimeoutException:
            print("Found the forbidden tile even though it shouldn't be showing up")
        self.verify_elements(elements)

    def verify_search(self):
        print("Checking the search...")

        driver.find_element(By.CLASS_NAME, "form-control").send_keys("Positive")
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
        tiles = ["The Benefits of Positive Thinking", "The Benefits of Volunteering"]
        for tile in tiles:
            try:
                h4 = driver.find_element(By.XPATH, f"//h4[contains(text(), '{tile}')]")
                h4.find_element(
                    By.XPATH, ".//span[@class='highlight' and contains(text(), 'Tile')]"
                )
                print(f"Found the {tile} tile")
            except NoSuchElementException:
                print(f"Couldn't find the {tile} tile")


bot = Subway_template_test()
if __name__ == "__main__":
    try:
        bot.login()
        bot.go_into_TESTdpt()
        bot.create_room(
            "Subway theme test",
            "As the world continues to face the challenges of climate change, the need for sustainable energy sources has never been more pressing.",
        )
        bot.create_tile(
            "The Benefits of Volunteering",
            "Volunteering is an amazing way to give back to our communities and make a positive impact in the world. It allows us to help others, learn new skills, and connect with like-minded individuals.",
        )
        bot.create_tile(
            "The Benefits of Learning a New Language",
            "Learning a new language is an amazing way to expand our horizons and connect with other cultures. It allows us to communicate with people from different parts of the world, and opens up new opportunities for travel, work, and personal growth.",
        )
        bot.create_room(
            "The Benefits of Travel",
            "Travel is an amazing way to broaden our horizons and experience new cultures. It allows us to step outside of our comfort zones and see the world from a different perspective.",
        )
        bot.create_tile(
            "The Importance of Regular Exercise",
            "Regular exercise is essential for maintaining good health and preventing chronic diseases. It can improve cardiovascular health, strengthen bones and muscles, and boost mental health.",
        )
        bot.create_tile(
            "The Benefits of Mindfulness Meditation",
            "Mindfulness meditation is a practice that involves focusing your attention on the present moment, without judgment. It has been shown to have numerous benefits for both physical and mental health.",
        )
        bot.add_file()
        bot.create_room(
            "The Benefits of Creative Expression",
            "Creative expression is an amazing way to explore our inner selves and share our unique perspectives with the world. Whether it’s through art, music, writing, or other forms of creativity, expressing ourselves creatively can have numerous benefits for our mental health and well-being.",
        )
        bot.create_forbidden_tile("Forbidden tile", "Forbidden description")
        bot.create_room(
            "The Benefits of Mindful Eating",
            "Mindful eating is the practice of paying attention to our food and the experience of eating. It involves being present in the moment, savoring the flavors and textures of our food, and listening to our body’s hunger and fullness cues.",
        )
        bot.create_tile(
            "The Benefits of Positive Thinking",
            "Positive thinking is the practice of focusing on the good in any situation and maintaining a positive outlook on life. It has been shown to have numerous benefits for our mental and physical health.",
        )
        bot.go_to_subway_theme_test()
        bot.open_website_publishing()
        bot.edit_appearance_and_publish()
        bot.verify_published_homepage()
        bot.verify_benefits_subroom()
        bot.verify_creative_expression_subroom()
        bot.verify_mindful_eating_subroom()
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
