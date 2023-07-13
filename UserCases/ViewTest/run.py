from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)
from view_test.view_test import View_test, driver
import time


try:
    with View_test() as bot:
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
