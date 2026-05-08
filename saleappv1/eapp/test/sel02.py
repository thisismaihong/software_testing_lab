#Tiki : https://tiki.vn/nha-sach-tiki/c8322

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

service =Service(executable_path='../../.venv/chromedriver.exe')
driver=webdriver.Chrome(service=service)
driver.get('https://tiki.vn/nha-sach-tiki/c8322')

#Cuộn trang để nạp dữ liệu
driver.execute_script("window.scrollTo(0,600)")
driver.implicitly_wait(1)

products=driver.find_elements(By.CLASS_NAME, "product-item")
page=[]

for p in products[:4]:
    print(p.get_attribute("href"))
    name=p.find_element(By.TAG_NAME,"h3")
    print(name.text)
    page.append(p.get_attribute("href"))
    print("=====================")


for idx, p in enumerate(page):
    print(f"\n----Comment sản phẩm {idx + 1}----")

    driver.get(p)
    driver.save_screenshot(f"product{idx}.png")

    driver.execute_script("window.scrollTo(0,5000)")
    driver.execute_script("window.scrollTo(0,2000)")
    driver.execute_script("window.scrollTo(0,2000)")
    driver.implicitly_wait(1)
    comments=driver.find_elements(By.CLASS_NAME, "review-comment__content")
    for idx,c in enumerate(comments):
        print(f"Comment {idx + 1}:", c.text)


driver.quit()

