from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()   # 声明浏览器对象
driver.get("https://www.baidu.com")
# print(driver)
# 定位文本框
# 方式 1:按照 id 属性查找定位到文本框
# searchTextBox = driver.find_element(By.ID, 'kw')
#
# # 方式 2: 按照 name 属性查找定位到文本框
# # searchTextBox = driver.find_element(By.NAME, 'wd')
#
# # 方式 3: 按照 class 属性查找定位到文本框
# # searchTextBox = driver.find_element(By.CLASS_NAME, 's_ipt')
#
#
# # 模拟用户输入行为
# searchTextBox.send_keys('')
#
# # 通过Xpath获取元素
# su_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="百度一下" and @class="bg s_btn"]')
#
# # 模拟用户点击行为
# su_button.click()
