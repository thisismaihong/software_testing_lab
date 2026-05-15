from selenium.webdriver.common.by import By

from eapp.test.pages.BasePage import BasePage

class LoginPage(BasePage):
    URL="http://127.0.0.1:5000/login"
    USERNAME=(By.ID , "username")
    PASSWORD=(By.ID,"pwd")
    LOGIN_BUTTON=(By.CSS_SELECTOR,".container form > div:nth-child(3) > button")

    def open_page(self, url=URL):
        self.open(url)

    def login(self, username, password):
        self.typing(*self.USERNAME, username)
        self.typing(*self.PASSWORD, password)
        self.click(*self.LOGIN_BUTTON)