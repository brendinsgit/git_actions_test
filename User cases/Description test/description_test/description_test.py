import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# browser = input("Enter your preferred browser (Firefox, Edge or Chrome): ")
webdriver_path = input("Enter the path to your Chrome webdriver: ")
email_address = input("Please provide an email that can be used to log in: ")
password = input("Please provide a password that can be used to log in: ")
os.environ["PATH"] += os.pathsep + webdriver_path
"""
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
"""

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options)


class Description_test:
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
        self.wait = WebDriverWait(self.driver, 30)
        os.environ["PATH"] += self.webdriver_path
        super(Description_test, self).__init__()

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
        WebDriverWait(self.driver, 10).until(
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
            "Description test room"
        )
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Add room')]")
            )
        ).click()

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
            "Description test room"
        )
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Add room')]")
            )
        ).click()

    def create_tile(self):
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
        ).send_keys("Description test tile")

    # In order to put in a description, we have to use JS scripts, because the description isn't an input or a text-area
    def headings(self):
        headings = ["Heading 1", "Heading 2", "Heading 3"]
        heading_tags = ["h2", "h3", "h4"]

        for heading, heading_tag in zip(headings, heading_tags):
            # Click the 'Heading' button
            driver.find_element(By.CLASS_NAME, "ck-button").click()
            driver.find_element(
                By.XPATH, f"//span[contains(text(), '{heading}')]"
            ).click()

            # Set the heading text
            heading_element = driver.find_element(
                By.CSS_SELECTOR, f"div.ck-content {heading_tag}"
            )
            driver.execute_script(
                f"arguments[0].textContent = '{heading}'", heading_element
            )

            # Move to the next line
            heading_element.send_keys(Keys.ENTER)

    def basic_font_manipulation(self):
        # Click the 'Paragraph' button
        driver.find_element(By.CLASS_NAME, "ck-button").click()
        driver.find_element(By.XPATH, "//span[contains(text(), 'Paragraph')]").click()

        # Click the 'Bold', 'Italic', and 'Underline' buttons
        for button_text in ["Bold", "Italic", "Underline"]:
            driver.find_element(
                By.XPATH, f"//button[.//span[text()='{button_text}']]"
            ).click()

        # Set the font background color to yellow
        driver.find_element(
            By.XPATH, "//button[.//span[text()='Font Background Color']]"
        ).click()
        driver.find_element(By.XPATH, "//button[.//span[text()='Yellow']]").click()

        # Set the text of the first paragraph
        p_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content p")
        first_paragraph = p_elements[0]
        driver.execute_script("arguments[0].textContent = 'Paragraph'", first_paragraph)

        # Move to the next line
        first_paragraph.send_keys(Keys.ARROW_DOWN)
        first_paragraph.send_keys(Keys.ENTER)

        # Unclick Bold, Italic, Underlined
        for button_text in ["Bold", "Italic", "Underline"]:
            driver.find_element(
                By.XPATH, f"//button[.//span[text()='{button_text}']]"
            ).click()

        # Get rid of the text background color
        driver.find_element(
            By.XPATH, "//button[.//span[text()='Font Background Color']]"
        ).click()
        driver.find_element(By.CLASS_NAME, "ck-color-table__remove-color").click()

        # Add the highlight
        driver.find_element(By.XPATH, "//button[.//span[text()='Highlight']]").click()

        # Write the second paragraph
        p_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content p")
        second_paragraph = p_elements[1]
        driver.execute_script(
            "arguments[0].textContent = 'Another paragraph'", second_paragraph
        )

        # Move to the next line
        second_paragraph.send_keys(Keys.ARROW_DOWN)
        second_paragraph.send_keys(Keys.ENTER)

    def size_manipulation(self):
        sizes = ["Tiny", "Small", "Big", "Huge"]
        paragraphs = [
            "Tiny paragraph",
            "Small paragraph",
            "Big paragraph",
            "Huge paragraph",
        ]

        # Unclick the highlight, yeah it only deselects when clicking twice seperately on it
        driver.find_element(By.XPATH, "//button[.//span[text()='Highlight']]").click()
        driver.find_element(By.XPATH, "//button[.//span[text()='Highlight']]").click()

        for size, paragraph_text in zip(sizes, paragraphs):
            # Change font size
            driver.find_element(
                By.XPATH, "//button[.//span[text()='Font Size']]"
            ).click()
            driver.find_element(By.XPATH, f"//button[.//span[text()='{size}']]").click()

            # Set paragraph text
            p_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content p")
            last_paragraph = p_elements[-1]
            driver.execute_script(
                f"arguments[0].textContent = '{paragraph_text}'", last_paragraph
            )

            # Create new line
            last_paragraph.send_keys(Keys.ARROW_DOWN)
            last_paragraph.send_keys(Keys.ENTER)

    # def link(self): TO DO: Add this link and make it work
    #    driver.find_element(By.CLASS_NAME, "ck-button").click()
    #    driver.find_element(By.XPATH, "//span[contains(text(), 'Paragraph')]").click()
    #    driver.find_element(By.XPATH, "//button[.//span[text()='Link']]").click()
    #    driver.find_element(By.CLASS_NAME, "ck-input-text").send_keys("google.com")
    def text_alignment(self):
        alignments = ["Align right", "Align center", "Justify"]
        paragraphs = ["Align right", "Align center", "Justify"]

        for alignment, paragraph_text in zip(alignments, paragraphs):
            # Click the 'Text alignment' button
            driver.find_element(
                By.XPATH, "//button[.//span[text()='Text alignment']]"
            ).click()
            driver.find_element(
                By.XPATH, f"//button[.//span[text()='{alignment}']]"
            ).click()

            # Set the paragraph text
            p_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content p")
            last_paragraph = p_elements[-1]
            driver.execute_script(
                f"arguments[0].textContent = '{paragraph_text}'", last_paragraph
            )

            # Move to the next line
            last_paragraph.send_keys(Keys.ARROW_DOWN)
            last_paragraph.send_keys(Keys.ENTER)

    # def lists(self): TO DO: Add this one too...
    # Unordered lists
    #    driver.find_element(
    #        By.XPATH, "//button[.//span[text()='Bulleted List']]"
    #    ).click()
    #    li_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content ul li")
    #    last_li = li_elements[-1]
    #    driver.execute_script(
    #        "arguments[0].textContent = 'Bulleted list item'", last_li
    #    )
    def subscript(self):
        # Set the paragraph text
        p_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content p")
        last_paragraph = p_elements[-1]
        driver.find_element(By.XPATH, "//button[.//span[text()='Subscript']]").click()
        driver.execute_script(f"arguments[0].textContent = 'Subscript'", last_paragraph)
        # Move to the next line
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)
        # Unclick the subscript
        driver.find_element(By.XPATH, "//button[.//span[text()='Subscript']]").click()

    def extra_items(self):
        def click_button(button_text):
            driver.find_element(
                By.XPATH, f"//button[.//span[text()='{button_text}']]"
            ).click()

        def set_last_paragraph_text(text):
            p_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content p")
            last_paragraph = p_elements[-1]
            driver.execute_script(
                f"arguments[0].textContent = '{text}'", last_paragraph
            )
            return last_paragraph

        # Click the 'Show more items' button
        click_button("Show more items")

        # Click the 'Superscript' button
        click_button("Superscript")

        # Set the text of the last paragraph to 'Superscript'
        last_paragraph = set_last_paragraph_text("Superscript")

        # Move to the next line
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

        # Click the 'Show more items' button
        click_button("Show more items")

        # Click the 'Superscript' button again
        click_button("Superscript")

        # Move to the next line
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

        click_button("Show more items")

        # Click the 'Special characters' button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[text()='Special characters']]")
            )
        ).click()

        # Set the text of the last paragraph to '₠'
        last_paragraph = set_last_paragraph_text("₠")

        # Move to the next line
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

        # Click the 'Strikethrough' button
        click_button("Strikethrough")

        # Set the text of the last paragraph to 'Crossed out text'
        last_paragraph = set_last_paragraph_text("Crossed out text")

        # Move to the next line
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

        # Click the 'Show more items' button
        click_button("Show more items")

        # Click the 'Strikethrough' button again
        click_button("Strikethrough")

        # Move to the next line
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

        # Click the 'Show more items' button
        click_button("Show more items")

        # Click the 'Templates' button
        click_button("Templates")

        # Click the 'Table for testing' button
        click_button("Table for testing")

    def finish_tile(self):
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add tile')]").click()

    def verify_tile(self):
        print("Time to see if everything is showing up....")

        def check_element(driver, by, value, description):
            try:
                driver.find_element(by, value)
                print(f"{description} found!")
            except NoSuchElementException:
                print(f"{description} not found.")

        # Check for headings
        check_element(
            driver,
            By.XPATH,
            "//h2[contains(text(), 'Heading 1')]",
            "H2 with text 'Heading 1'",
        )

        check_element(
            driver,
            By.XPATH,
            "//h3[contains(text(), 'Heading 2')]",
            "H3 with text 'Heading 2'",
        )

        check_element(
            driver,
            By.XPATH,
            "//h4[contains(text(), 'Heading 3')]",
            "H4 with text 'Heading 3'",
        )

        # Check for bold, italic, underlined with BG color
        check_element(
            driver,
            By.XPATH,
            "//p/span[@style='background-color:hsl(60, 75%, 60%);']/i/strong/u",
            "P containing span with style 'background-color:hsl(60, 75%, 60%)' containing i containing strong containing u",
        )

        # Check for highlighted
        check_element(
            driver,
            By.XPATH,
            "//mark[@class='marker-yellow'][contains(text(), 'Another paragraph')]",
            "Mark with class 'marker-yellow' and text 'Another paragraph'",
        )

        # Check for Font sizes
        check_element(
            driver,
            By.XPATH,
            "//span[@class='text-tiny'][contains(text(), 'Tiny paragraph')]",
            "Span with class 'text-tiny' and text 'Tiny paragraph'",
        )

        check_element(
            driver,
            By.XPATH,
            "//span[@class='text-small'][contains(text(), 'Small paragraph')]",
            "Span with class 'text-small' and text 'Small paragraph'",
        )

        check_element(
            driver,
            By.XPATH,
            "//span[@class='text-big'][contains(text(), 'Big paragraph')]",
            "Span with class 'text-big' and text 'Big paragraph'",
        )

        check_element(
            driver,
            By.XPATH,
            "//span[@class='text-huge'][contains(text(), 'Huge paragraph')]",
            "Span with class 'text-huge' and text 'Huge paragraph'",
        )

        # Check for text alignment
        check_element(
            driver,
            By.XPATH,
            "//p[@style='text-align:right;']/span[@class='text-huge'][contains(text(), 'Align right')]",
            "P with style 'text-align:right' containing span with class 'text-huge' and text 'Align right'",
        )

        check_element(
            driver,
            By.XPATH,
            "//p[@style='text-align:center;']/span[@class='text-huge'][contains(text(), 'Align center')]",
            "P with style 'text-align:center' containing span with class 'text-huge' and text 'Align center'",
        )

        check_element(
            driver,
            By.XPATH,
            "//p[@style='text-align:justify;']/span[@class='text-huge'][contains(text(), 'Justify')]",
            "P with style 'text-align:justify' containing span with class 'text-huge' and text 'Justify'",
        )

        # Check for subscript
        check_element(
            driver,
            By.XPATH,
            "//sub[contains(text(), 'Subscript')]",
            "Sub element with text 'Subscript'",
        )

        # Check for superscript
        check_element(
            driver,
            By.XPATH,
            "//sup[contains(text(), 'Superscript')]",
            "Sup element with text 'Superscript'",
        )

        # Check for span with "₠"
        check_element(
            driver,
            By.XPATH,
            "//span[contains(text(), '₠')]",
            "Span with text '₠'",
        )

        # Check for crossed out text
        check_element(
            driver,
            By.XPATH,
            "//s[contains(text(), 'Crossed out text')]",
            "S element with text 'Crossed out text'",
        )
        # Check if there is a table
        check_element(driver, By.XPATH, "//table", "Table")
