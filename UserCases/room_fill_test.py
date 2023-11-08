import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)


webdriver_path = ChromeDriverManager().install()
email_address = "max.gapa+automation_tests@kenja.com"
password = "automation_testing1234"
image_source = "D:/a/rooms3-selenium-tests/rooms3-selenium-tests/TestFiles/doggo.png"
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
driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))

class Room_fill_test:
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
        self.img_src = image_source
        self.wait = WebDriverWait(self.driver, 30)
        os.environ["PATH"] += self.webdriver_path
        super(Room_fill_test, self).__init__()

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

    def open_create_room(self):
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
            "test room"
        )

    def profile_picture_testing(self):
        # Add avatar
        avatar_path = f"{self.img_src}"
        driver.find_element(By.XPATH, "//input[@name='avatar']").send_keys(avatar_path)
        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "crop-image-preview"))
        )

        # Save avatar
        save_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))
        )
        save_button.click()

        # Check if avatar was added successfully
        driver.implicitly_wait(10)
        try:
            pic_slot = driver.find_element(
                By.CSS_SELECTOR, ".avatar-preview.avatar.huge.drop-zone"
            )
            img = pic_slot.find_element(By.TAG_NAME, "img")
            img_src = img.get_attribute("src")
            if img_src:
                print("The avatar slot appears to have an image inside it")
            else:
                print("The avatar slot is missing an image")
        except NoSuchElementException:
            print("The slot or the image inside the slot wasn't located")

        # Choose image
        driver.find_element(By.LINK_TEXT, "Chose image").click()
        search_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@name='search'][@class='form-control filter'][@placeholder='Search by name']",
                )
            )
        )
        search_input.send_keys("Support")

        # Check for support paragraph
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(text(), 'Support')]")
                )
            )
            print("Found the support paragraph")
        except:
            print("Couldn't find the support paragraph")

        # Clear search input and press enter
        search_input.clear()
        search_input.send_keys(Keys.ENTER)

        # Click on link and security paragraph
        driver.find_element(By.LINK_TEXT, "14").click()
        driver.find_element(By.XPATH, "//p[contains(text(), 'Security')]").click()

    def set_sharing(self):
        self.wait.until(EC.visibility_of_element_located((By.ID, "data-sharing")))
        Select(driver.find_element(By.ID, "data-sharing")).select_by_visible_text(
            "Share as parent room"
        )

    def test_headings(self):
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
        # Set font color
        # driver.find_element(By.XPATH, "//button[.//span[text()='Font Color']]").click()
        # driver.find_element(By.XPATH, "//button[.//span[text()='Turquoise']]").click()

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

    def move_to_next_line(self):
        p_elements = driver.find_elements(By.CSS_SELECTOR, "div.ck-content p")
        last_paragraph = p_elements[-1]
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

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
        # Set back to default
        driver.find_element(By.XPATH, "//button[.//span[text()='Font Size']]").click()
        driver.find_element(By.XPATH, f"//button[.//span[text()='Default']]").click()

    def link(self):
        driver.find_element(By.XPATH, "//button[.//span[text()='Link']]").click()
        driver.find_element(
            By.XPATH, "//div[@class='ck ck-labeled-field-view__input-wrapper']/input"
        ).send_keys("https://www.google.com/")
        driver.find_element(
            By.XPATH,
            "//form[@class='ck ck-link-form ck-responsive-form']//button[span[text()='Save']]",
        ).click()

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

        click_button("Show more items")

        click_button("Subscript")

        # Set the text of the last paragraph to 'Subscript'
        last_paragraph = set_last_paragraph_text("Subscript")

        # Move to the next line
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

        click_button("Show more items")

        # Click the 'Subscript' button again to remove it
        click_button("Subscript")

        # Move to the next line
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

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
        self.wait.until(
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

        click_button("Show more items")

        click_button("Block quote")
        last_paragraph = set_last_paragraph_text("Beautiful Quote")

        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

        click_button("Show more items")
        # Unclick
        click_button("Block quote")

        # Click the 'Show more items' button
        click_button("Show more items")

        # Click the 'Templates' button
        click_button("Templates")

        # Click the 'Table for testing' button
        click_button("Table for testing")

    def test_table(self):
        input_place = driver.find_element(
            By.XPATH,
            "//td[@class='ck-editor__editable ck-editor__nested-editable']/span",
        )
        driver.execute_script("arguments[0].textContent = 'Paragraph'", input_place)
        input_place.click()

    def finish_room(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Add room']"))
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
        ).send_keys("test tile")

    def extra_items_tile(self):
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

        click_button("Subscript")

        # Set the text of the last paragraph to 'Subscript'
        last_paragraph = set_last_paragraph_text("Subscript")
        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)
        click_button("Subscript")
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
        self.wait.until(
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

        click_button("Show more items")

        click_button("Block quote")
        last_paragraph = set_last_paragraph_text("Beautiful Quote")

        last_paragraph.send_keys(Keys.ARROW_DOWN)
        last_paragraph.send_keys(Keys.ENTER)

        click_button("Show more items")
        # Unclick
        click_button("Block quote")

        # Click the 'Show more items' button
        click_button("Show more items")

        # Click the 'Templates' button
        click_button("Templates")

        # Click the 'Table for testing' button
        click_button("Table for testing")

    def finish_tile(self):
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add tile')]").click()

    def verify_room(self):
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
            "//p[@style='text-align:right;'][contains(text(), 'Align right')]",
            "P with style 'text-align:right' and text 'Align right'",
        )

        check_element(
            driver,
            By.XPATH,
            "//p[@style='text-align:center;'][contains(text(), 'Align center')]",
            "P with style 'text-align:center' containing span with class 'text-huge' and text 'Align center'",
        )

        check_element(
            driver,
            By.XPATH,
            "//p[@style='text-align:justify;'][contains(text(), 'Justify')]",
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
            "//p[contains(text(), '₠')]",
            "Span with text '₠'",
        )

        # Check for crossed out text
        check_element(
            driver,
            By.XPATH,
            "//s[contains(text(), 'Crossed out text')]",
            "S element with text 'Crossed out text'",
        )
        check_element(
            driver,
            By.XPATH,
            "//a[@href='https://www.google.com/']",
            "<a> element with href 'https://www.google.com/'",
        )
        check_element(
            driver,
            By.XPATH,
            "//blockquote[contains(., 'Beautiful Quote')]",
            "<blockquote> with text content 'Beautiful Quote'",
        )
        check_element(
            driver,
            By.XPATH,
            "//td[contains(., 'Paragraph')]",
            "<td> with text content 'Paragraph'",
        )
        # Check if there is a table
        check_element(driver, By.XPATH, "//table", "Table")

    def go_back(self):
        # Wait for the modal-backdrop fade to disappear
        self.wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        driver.find_element(
            By.XPATH,
            "//span[@class='breadcrumb-label' and contains(text(), 'TEST dpt')]",
        ).click()

    def create_forbidden_tile(self):
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
        ).send_keys("forbidden tile")
        driver.find_element(By.ID, "data-important").click()
        driver.find_element(By.ID, "data-publish_locked").click()

    def check_if_pinned(self):
        element = driver.find_element(
            By.CSS_SELECTOR, ".object.object-important .object-wrapper"
        )
        color = element.value_of_css_property("border-top-color")
        hex_color = Color.from_string(color).hex

        if hex_color == "#940000":
            print("The border top color is #940000, which ensures the tile is pinned")
        else:
            print(
                "The border top color is not #940000, as it should be for a pinned tile"
            )

    def check_website_publishing(self):
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
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Content"))).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".publish-room-item-expand .glyphicon.glyphicon-plus")
            )
        ).click()
        try:
            driver.find_element(By.CSS_SELECTOR, ".glyphicon.glyphicon-lock")
            print("Found locked room in content tab")
        except NoSuchElementException:
            print(
                "Couldn't find locked room in content tab. Tried to look for a span with class 'glyphicon-lock'"
            )


bot = Room_fill_test()
if __name__ == "__main__":
    try:
        bot.login()
        bot.open_create_room()
        bot.profile_picture_testing()
        bot.set_sharing()

        bot.test_headings()
        bot.move_to_next_line()
        bot.basic_font_manipulation()
        bot.size_manipulation()
        bot.move_to_next_line()
        bot.link()
        bot.move_to_next_line()
        bot.text_alignment()
        bot.move_to_next_line()
        bot.extra_items()
        bot.test_table()
        bot.finish_room()

        bot.create_tile()
        bot.test_headings()
        bot.move_to_next_line()
        bot.basic_font_manipulation()
        bot.size_manipulation()
        bot.move_to_next_line()
        bot.link()
        bot.move_to_next_line()
        bot.text_alignment()
        bot.extra_items_tile()
        bot.test_table()
        bot.finish_tile()
        print("TILE RESULTS")
        bot.verify_room()
        bot.go_back()
        print("ROOM RESULTS")
        bot.verify_room()
        bot.create_forbidden_tile()
        bot.finish_tile()
        bot.check_if_pinned()
        bot.check_website_publishing()
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
