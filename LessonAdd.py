from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import json
import time

# 文件夹路径
dir_path = r"G:\汉语言文学\23考前精品班文科6班\23现代汉语 寒假班 齐靖"

# 列出文件夹下的所有文件
files = os.listdir(dir_path)

browser = webdriver.Chrome()
browser.get('https://www.qingxuetang.com/admin/course/HjGtPec5G4g/lesson/add')

with open('qingxuetang_cookies.txt', 'r', encoding='utf-8') as f:
    cookies = json.load(f)

for cookie in cookies:
    if 'expiry' in cookie:  # 如果cookie项中包含'expiry'项，需要删除，因为可能导致加载失败
        del cookie['expiry']
    if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
        cookie['sameSite'] = "None"  # 如果 'sameSite' 的值不在 ["Strict", "Lax", "None"] 中，将其设置为 "None"
    browser.add_cookie(cookie)

browser.refresh()

# 遍历所有文件
for file_name in files:
    file_path = os.path.join(dir_path, file_name)  # 获取完整的文件路径

    upload_button = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '视频')]"))
    )
    upload_button.click()

    upload = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    )
    upload.send_keys(file_path)

    upload_success = WebDriverWait(browser, 1200).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "上传成功！")]'))
    )

    save_button = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "保存")]'))
    )
    save_button.click()

    add_button = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "添加课时")]'))
    )
    add_button.click()

