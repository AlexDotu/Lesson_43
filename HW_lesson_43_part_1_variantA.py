import random
import time

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException, ElementNotInteractableException,
    StaleElementReferenceException, ElementClickInterceptedException)
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

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="__cookiesNlink __cookiesSuccess"]'))
        ).click()
    except ElementClickInterceptedException:
        print("Не удалось нажать на кнопку согласия с куки")

    try:

        categories = driver.find_elements(By.XPATH, "//li[@class='mega-drop-down']")
        if categories:
            random_category = random.choice(categories)
            category_url = random_category.find_element(By.TAG_NAME, "a").get_attribute("href")

            driver.get(category_url)
            time.sleep(4)
            print("Категория успешно открыта.")
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
                except (
                        ElementClickInterceptedException, ElementNotInteractableException,
                        StaleElementReferenceException):
                    print("Элемент не кликабелен, пропускаем")
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
                    next_page_button = driver.find_element(By.XPATH, ".//a[@class='btn j-more-products nextProducts']")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_page_button)
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, ".//a[@class='btn j-more-products nextProducts']"))
                    )
                    driver.execute_script("arguments[0].click();", next_page_button)
                    time.sleep(2)
                except NoSuchElementException:
                    print("Следующих страниц нет.")
                    break

        print("Добавление товаров в корзину завершено.")

        cart_count_element = driver.find_element(By.XPATH, "//span[@id='checkout_items']")
        cart_count = int(cart_count_element.text)

        if cart_count != added_products:
            print(
                f"Ошибка: число товаров в корзине ({cart_count}) не совпадает с числом добавленных ({added_products}).")
        else:
            print("Число товаров на значке корзины совпадает с числом добавленных товаров.")

        cart_button = driver.find_element(By.XPATH, "//li[@class='checkout cartLink']/a")
        driver.execute_script("arguments[0].click();", cart_button)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='overtable basketControl detailAdd']"))
        )

        cart_items = driver.find_elements(By.XPATH,
                                          "//table[@class='table table-responsive shopping-cart-table']//tbody/tr")
        print(f"Количество товаров в корзине: {len(cart_items)}")
        if len(cart_items) >= total_product_count:
            print("Товары успешно добавлены в корзину.")
        else:
            print("Некоторые товары не были добавлены в корзину.")

        time.sleep(5)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()


add_to_cart_test()
