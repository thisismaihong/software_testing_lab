import time

from selenium.webdriver.common.by import By

from eapp.test.test_base import driver, test_app



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

