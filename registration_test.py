import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка логирования
logging.basicConfig(filename='test_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# Тест регистрации нового клиента
def test_registration(driver):
    driver.get("https://.../register")

    # Корректные данные
    driver.find_element(By.ID, "firstName").send_keys("Иван")
    driver.find_element(By.ID, "lastName").send_keys("Иванов")
    driver.find_element(By.ID, "patronymic").send_keys("Иванович")
    driver.find_element(By.ID, "birthday").send_keys("02.01.1999")
    driver.find_element(By.ID, "email").send_keys("ivanov@test.com")
    driver.find_element(By.ID, "phone").send_keys("+79123456789")
    driver.find_element(By.ID, "register_button").click()

    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "success_message"))
    )
    assert success_message.text == "Регистрация успешна"
    logging.info("Тест регистрации пройден успешно.")

    # Пустые поля
    driver.get("https://.../register")
    driver.find_element(By.ID, "register_button").click()
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "error_message"))
    )
    assert "Все поля обязательны для заполнения" in error_message.text
    logging.info("Тест регистрации с пустыми полями пройден успешно.")

    # Некорректный email
    driver.get("https://.../register")
    driver.find_element(By.ID, "firstName").send_keys("Иван")
    driver.find_element(By.ID, "lastName").send_keys("Иванов")
    driver.find_element(By.ID, "patronymic").send_keys("Иванович")
    driver.find_element(By.ID, "birthday").send_keys("02.01.1999")
    driver.find_element(By.ID, "email").send_keys("ivanov.test.com")
    driver.find_element(By.ID, "phone").send_keys("+79123456789")
    driver.find_element(By.ID, "register_button").click()
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "error_message"))
    )
    assert "Некорректный email" in error_message.text
    logging.info("Тест регистрации с некорректным email пройден успешно.")


# Тест авторизации клиента
def test_login(driver):
    driver.get("https://.../login")

    driver.find_element(By.ID, "email").send_keys("ivanov@test.com")
    driver.find_element(By.ID, "password").send_keys("123456789")
    driver.find_element(By.ID, "login_button").click()

    dashboard = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dashboard"))
    )
    assert dashboard.is_displayed()
    logging.info("Тест авторизации пройден успешно.")

    # Проверка входа с некорректными данными
    driver.get("https://.../login")
    driver.find_element(By.ID, "email").send_keys("ivanov.test.com")
    driver.find_element(By.ID, "password").send_keys("WrongPass123")
    driver.find_element(By.ID, "login_button").click()

    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "error_message"))
    )
    assert error_message.text == "Неверный email или пароль"
    logging.info("Тест некорректной авторизации пройден успешно.")


# Тест создания заявки на кредит
def test_apply_loan(driver):
    driver.get("https://.../apply-loan")

    driver.find_element(By.ID, "type").send_keys("consumer")
    driver.find_element(By.ID, "amount").send_keys("100000")
    driver.find_element(By.ID, "term").send_keys("12")
    driver.find_element(By.ID, "income").send_keys("50000")
    driver.find_element(By.ID, "submit_button").click()

    status = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "status"))
    )
    assert "Заявка отправлена" in status.text
    logging.info("Тест заявки на кредит пройден успешно.")