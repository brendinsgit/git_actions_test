from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)

from task_tests.task_tests import Task_tests, driver

try:
    with Task_tests() as bot:
        bot.login()
        bot.create_room()
        bot.create_tile()
        bot.create_task()
        bot.verify_tile()
        # bot.write_comment()
        bot.check_side_bar()
        bot.send_email_reminder()
        bot.add_subtask()
        bot.delete_subtask()
        bot.go_to_dashboard()
        bot.check_if_task_shows_up()
        bot.check_if_room_shows_up()
        bot.check_rooms_tab()
        bot.check_tasks_tab()
        bot.go_to_dashboard()
        bot.delete_room()
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
