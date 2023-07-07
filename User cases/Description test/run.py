from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)
from description_test.description_test import Description_test, driver
import time

try:
    with Description_test() as bot:
        bot.login()
        bot.create_room()
        bot.create_tile()
        bot.headings()
        bot.basic_font_manipulation()
        bot.size_manipulation()
        # bot.link()
        bot.text_alignment()
        # bot.lists()
        bot.subscript()
        bot.extra_items()
        bot.finish_tile()
        bot.verify_tile()

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
