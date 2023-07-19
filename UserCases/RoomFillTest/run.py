from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)
from room_fill_test.room_fill_test import Room_fill_test, driver
import time

try:
    with Room_fill_test() as bot:
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
