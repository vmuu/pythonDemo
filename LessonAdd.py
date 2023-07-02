from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import threading

# 文件夹路径
dir_path = r"G:\2023云南专升本考前急救包（高等数学）【直播课】"

# 列出文件夹下的所有文件
files = os.listdir(dir_path)

# 创建锁对象
lock = threading.Lock()

# 已上传的文件集合
uploaded_files = set()


# 定义上传文件的函数
def upload_file(file_path):
    # 创建浏览器实例
    browser = webdriver.Chrome()

    # 打开上传网址
    browser.get('https://www.qingxuetang.com/admin/course/KD22QM_73HM/lesson/add')

    # 读取cookies
    with open('qingxuetang_cookies.txt', 'r', encoding='utf-8') as f:
        cookies = json.load(f)

    # 添加cookies
    for cookie in cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        if 'sameSite' in cookie and cookie['sameSite'] not in ["Strict", "Lax", "None"]:
            cookie['sameSite'] = "None"
        browser.add_cookie(cookie)

    # 刷新页面使cookie生效
    browser.refresh()

    while True:
        # 等待页面加载完成，点击视频按钮
        upload_button = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '视频')]"))
        )
        upload_button.click()

        # 上传文件
        upload = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        upload.send_keys(file_path)

        # 等待上传完成
        upload_success = WebDriverWait(browser, 1200).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "上传成功！")]'))
        )

        # 检测到页面上传成功提示后，点击保存按钮
        save_button = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "保存")]'))
        )
        save_button.click()

        # 等待页面跳转完成，出现添加课时按钮并点击
        add_button = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "添加课时")]'))
        )
        add_button.click()

        # 等待页面加载完成，重新开始上传循环
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '视频')]"))
        )

        # 检查是否还有其他文件需要上传
        with lock:
            if files:
                next_file_name = files.pop(0)
        if next_file_name:
            next_file_path = os.path.join(dir_path, next_file_name)  # 获取完整的文件路径
            with lock:
                if next_file_name not in uploaded_files:
                    uploaded_files.add(next_file_name)
                    file_path = next_file_path
                else:
                    break
        else:
            break

    # 关闭浏览器
    browser.quit()


# 同时上传多个文件的函数
def upload_files():
    while True:
        file_name = None
        with lock:
            if files:
                file_name = files.pop(0)
        if file_name:
            file_path = os.path.join(dir_path, file_name)  # 获取完整的文件路径
            with lock:
                if file_name not in uploaded_files:
                    uploaded_files.add(file_name)
            upload_file(file_path)
        else:
            break


# 创建线程列表
threads = []

# 创建并启动多个上传线程
for _ in range(3):  # 设置为3个线程
    t = threading.Thread(target=upload_files)
    t.start()
    threads.append(t)

# 等待所有线程完成
for t in threads:
    t.join()
