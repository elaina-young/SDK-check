#在终端下载selenium：pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 初始化WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# 登录功能
def login(username, password):
    driver.get('https://mit.s.dk/studiebolig/login/')  # 替换为登录页面URL
    time.sleep(2)
    
    username_field = driver.find_element(By.ID, 'id_username')
    password_field = driver.find_element(By.ID, 'id_password')  # 假设密码输入框的ID为 'id_password'
    
    username_field.send_keys(username)
    password_field.send_keys(password)
    
    login_button = driver.find_element(By.ID, 'id_login')  # 根据实际情况修改选择器
    login_button.click()
    time.sleep(5)  # 等待登录完成

# 展开主房屋列表
def expand_main_property_list():
    main_expand_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-toggle="collapse"]'))  # 根据实际情况修改选择器
    )
    main_expand_button.click()
    time.sleep(2)  # 等待列表展开

# 展开所有房屋列表
def expand_all_properties():
    while True:
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Vis flere ejendomme")]'))
            )
            try:
                show_more_button.click()
            except Exception as e:
                print(f"Retry clicking with JavaScript due to: {e}")
                driver.execute_script("arguments[0].click();", show_more_button)
            time.sleep(2)  # 等待列表展开
        except Exception as e:
            print("No more 'Vis flere ejendomme' button found or other error:", e)
            break

# 获取所有房屋链接
def get_property_links():
    driver.get('https://mit.s.dk/studiebolig/home/')  # 替换为包含房屋列表的页面URL
    time.sleep(2)
    
    expand_main_property_list()
    expand_all_properties()
    
    property_elements = driver.find_elements(By.CSS_SELECTOR, '.list-group-item.list-group-item-action')
    property_links = [elem.get_attribute('href') for elem in property_elements]
    return property_links

# 展开房屋详细信息的排队情况
def expand_queue_info():
    queue_expand_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.group-toggle-link'))  # 根据实际情况修改选择器
    )
    queue_expand_button.click()
    time.sleep(2)  # 等待排队信息展开

# 获取房屋详细信息
def get_queue_info(property_link):
    driver.get(property_link)
    time.sleep(2)
    
    expand_queue_info()
    
    # 查找包含A等级的图标
    queue_info_elements = driver.find_elements(By.CSS_SELECTOR, 'span.waiting-list-category')
    has_A = any('A' in elem.text for elem in queue_info_elements)
    
    return has_A

# 主函数
def main(username, password):
    login(username, password)
    
    property_links = get_property_links()
    filtered_properties = {}
    
    for link in property_links:
        if get_queue_info(link):
            filtered_properties[link] = True
    
    # 打印结果
    for link in filtered_properties:
        print(f"Property: {link} - Has 'A': Yes")

    driver.quit()

# 调用主函数
if __name__ == "__main__":
    main('你的用户名', '你的密码')  # 替换为实际的用户名和密码
