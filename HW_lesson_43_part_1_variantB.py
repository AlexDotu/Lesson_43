import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def add_to_cart_test():
    driver.get(url="https://www.dracek.cz/")
    time.sleep(3)

    driver.find_element(By.XPATH, '//a[@class="__cookiesNlink __cookiesSuccess"]').click()
    time.sleep(3)

    try:
        categories = driver.find_elements(By.XPATH, "//li[@class='mega-drop-down']")
        if categories:
            random_category = random.choice(categories)
            random_category.click()
            time.sleep(4)
            print("Категория выбрана.")
        else:
            print("Категории не найдены.")
            driver.quit()
            exit()

        added_products = 0
        total_product_count = 5

        while added_products < total_product_count:

            add_to_cart_buttons = driver.find_elements(By.XPATH, "//a[@class='btn main-action buyButton']")

            for add_to_cart_button in add_to_cart_buttons[added_products:]:
                if added_products >= total_product_count:
                    break

                try:

                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
                    driver.execute_script("arguments[0].click();", add_to_cart_button)
                except (ElementNotInteractableException, StaleElementReferenceException):
                    continue

                try:
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//a[@class='btn modalGreyButton btn-lg dCloseModal']"))
                    )
                    time.sleep(1)
                    back_button = driver.find_element(By.XPATH, "//a[@class='btn modalGreyButton btn-lg dCloseModal']")
                    driver.execute_script("arguments[0].click();", back_button)
                except (NoSuchElementException, ElementNotInteractableException):
                    continue

                added_products += 1

            if added_products < total_product_count:
                try:

                    next_page_button = driver.find_element(By.XPATH,
                                                           "//li[@class='pg_step']/a[@data-page][i[contains(@class, 'fa-chevron-right')]]")
                    driver.execute_script("arguments[0].click();", next_page_button)
                    time.sleep(3)
                    print('==clicked')
                except NoSuchElementException:
                    print("Следующая страница недоступна.")
                    break

        print("Добавление товаров в корзину завершено.")

        try:
            cart_count_element = driver.find_element(By.ID, "checkout_items")
            cart_count = int(cart_count_element.text)
            print(f"Количество товаров в корзине: {cart_count}")
            print(f"Количество добавленных товаров: {added_products}")

            if cart_count == added_products:
                print("Количество товаров в корзине соответствует ожидаемому.")
            else:
                print("Ошибка: количество товаров в корзине не соответствует количеству добавленных товаров.")

        except NoSuchElementException:
            print("Не удалось найти элемент с количеством товаров в корзине.")

        time.sleep(5)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()


add_to_cart_test()
