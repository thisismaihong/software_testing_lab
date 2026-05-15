import time
from ctypes.wintypes import tagMSG

import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from eapp.test.pages.CartPage import CartPage
from eapp.test.pages.LoginPage import LoginPage
from eapp.test.pages.RegisterPage import RegisterPage
from eapp.test.test_base import driver, test_app
from eapp.test.pages.HomePage import HomePage


def test_search_products(driver):
    driver.get("http://127.0.0.1:5000/")
    #Ô tìm kiếm
    e=driver.find_element(By.CSS_SELECTOR,"#collapsibleNavbar > form > input")
    kw="iPhone"
    e.send_keys(kw) #Từ nhập trong ô tìm kiếm
    driver.find_element(By.CSS_SELECTOR,"#collapsibleNavbar > form > button").click()
    time.sleep(1)

    results=driver.find_elements(By.CSS_SELECTOR, ".container .card-title")

    assert all (kw in r.text for r in results)

def test_login_success(driver):
    login=LoginPage(driver=driver)
    login.open_page()
    login.login(username="admin", password="123456")
    time.sleep(2)
    assert driver.current_url=="http://127.0.0.1:5000/"
    e=driver.find_element(By.CSS_SELECTOR, "#collapsibleNavbar > ul > li:nth-child(5) > a")
    assert (f"Chào admin" in e.text)


def test_pay_success(driver):
    home=HomePage(driver=driver)
    home.open_page()
    home.add()
    time.sleep(1)

    login = LoginPage(driver=driver)
    login.open_page()
    login.login(username="admin", password="123456")
    time.sleep(2)

    cart=CartPage(driver=driver)
    cart.open_page()
    cart.pay()
    time.sleep(1)

    with pytest.raises(NoSuchElementException):
        driver.find_element(By.TAG_NAME, "table")



def test_update_cart(driver):
    home = HomePage(driver=driver)
    home.open_page()
    home.add()
    time.sleep(1)

    login = LoginPage(driver=driver)
    login.open_page()
    login.login(username="admin", password="123456")
    time.sleep(2)

    cart = CartPage(driver=driver)
    cart.open_page()
    cart.update_cart_item(3)

    driver.implicitly_wait(3)
    e=driver.find_element(By.CLASS_NAME, "cart-counter")
    assert int(e.text)==3


def test_register(driver):
    register=RegisterPage(driver=driver)
    register.open_page()
    register.register(name="demo", username="demodemo", password="Abc@1234", confirm="Abc@1234", avatar=r"D:\software_testing_lab\saleappv1\eapp\test\product0.png")
    time.sleep(1)

    login = LoginPage(driver=driver)
    login.open_page()
    login.login(username="demodemo", password="Abc@1234") 
    time.sleep(1)

    assert driver.current_url=="http://127.0.0.1:5000/"
    e = driver.find_element(By.CSS_SELECTOR, "#collapsibleNavbar > ul > li:nth-child(5) > a")
    assert (f"Chào demodemo" in e.text)

