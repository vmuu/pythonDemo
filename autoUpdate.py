from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import json
import time

chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
  "download.default_directory": r"G:\新增课本\2023-05-31 TTB\地理学有志飞跃集训营习题册【处理后】",  # 修改为你的下载路径
  "download.prompt_for_download": False,  # 设置为False以禁用下载提示
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

browser = webdriver.Chrome(options=chrome_options)
browser.get('https://pan.baidu.com/aipan/uploadimg?key=ai_tools_to_write')

with open('cookies.txt', 'r', encoding='utf-8') as f:
    cookies = json.load(f)

for cookie in cookies:
    if 'expiry' in cookie:  # 如果cookie项中包含'expiry'项，需要删除，因为可能导致加载失败
        del cookie['expiry']
    if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
        cookie['sameSite'] = "None"  # 如果 'sameSite' 的值不在 ["Strict", "Lax", "None"] 中，将其设置为 "None"
    browser.add_cookie(cookie)

# Your file path
file_dir = r"G:\新增课本\2023-05-31 TTB\地理学有志飞跃集训营习题册"

# 获取文件夹下所有文件
files = os.listdir(file_dir)

for file in files:
    file_path = os.path.join(file_dir, file)
    if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):  # 检查是否是图片文件
        browser.refresh()  # 刷新页面，以清除上一次的上传结果

        time.sleep(2)
        upload = browser.find_element(By.XPATH, '//input[@type="file"]')
        upload.send_keys(file_path)
        upload_button = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '保存图片')]"))
        )
        upload_button.click()
        time.sleep(2)  # 等待下载完成

# browser.quit()  # 退出浏览器
