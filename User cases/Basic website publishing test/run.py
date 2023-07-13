from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)
from publishing_test.publishing_test import Publishing_test, driver


try:
    with Publishing_test() as bot:
        bot.login()
        bot.create_room()
        bot.create_first_tile()
        bot.create_second_tile()
        bot.add_file()
        bot.publish_room()
        bot.verify_published_page()
        bot.verify_search()

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
