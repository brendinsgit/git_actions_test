from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)
from sidebar_template_test.sidebar_temp_test import Sidebar_template_test, driver
import time

try:
    with Sidebar_template_test() as bot:
        bot.login()
        bot.go_into_TESTdpt()
        bot.create_room(
            "Sidebar theme test",
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
        bot.go_to_sidebar_theme_test()
        bot.open_website_publishing()
        bot.edit_appearance_and_publish()
        bot.verify_published_homepage()
        bot.verify_benefits_subroom()
        bot.verify_creative_expression_subroom()
        bot.verify_mindful_eating_subroom()
        bot.verify_nesting()
        # bot.verify_search() Can't interact with search-bar
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
