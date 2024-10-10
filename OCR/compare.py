'''
本方法基于Windows的API
需要手机投屏/模拟器来操作
所有的坐标参数都需要按照您自己系统来填写
本文件只支持比大小
'''

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import cv2
import numpy as np
import pyautogui
from paddleocr import PaddleOCR

import keyboard
import sys
import time

# 初始化 PaddleOCR 识别器
reader = PaddleOCR(use_angle_cls=False, lang='en')

not_found_count = 0
last_not_found_time = 0
draw_duration = 0.000

def capture_area():
    region = (25, 180, 540, 460)  # 识别区域的坐标
    screenshot = pyautogui.screenshot(region=region)
    return np.array(screenshot)

def recognize_numbers(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 使用 PaddleOCR 进行文本识别
    result = reader.ocr(gray, cls=False)

    try:
        text = ' '.join([item[1][0] for line in result for item in line])  # 提取识别出的文本
    except:
        text = ""
    
    # 处理识别的文本，提取数字
    for i in range(len(text.split("\n"))):
        nums = [int(s) for s in text.split("\n")[i].split() if s.isdigit()]
        if len(nums) == 3 and nums[1] == 7:
            return [nums[0], nums[1]]
        return nums

def draw_comparison(numbers):
    global not_found_count, last_not_found_time

    if len(numbers) < 2 or len(numbers) and max(numbers) > 100:
        current_time = time.time()
        if not_found_count == 0 or current_time - last_not_found_time > 1:
            not_found_count = 1
        else:
            not_found_count += 1
        last_not_found_time = current_time
        print("未找到足够的数字进行比较或检测到错误数字")

        if not_found_count >= 10 or len(numbers) and max(numbers) > 100:
            time.sleep(3)
            pyautogui.click(268, 534)  # “开心收下”按钮的坐标
            time.sleep(0.3)
            pyautogui.click(394, 979)  # “继续”按钮的坐标
            time.sleep(0.3)
            pyautogui.click(296, 858)  # “继续PK”按钮的坐标
            time.sleep(12)
            
            print("准备重新开始程序...")
            time.sleep(0.5)
            main()
        return

    first, second = numbers[0], numbers[1]
    origin_x, origin_y = 180, 650  # 绘制区域的坐标
    size = 50



    if first > second:
        print(f"{first} > {second}")
        draw_greater_than(origin_x, origin_y, size)
    elif first < second:
        print(f"{first} < {second}")
        draw_less_than(origin_x, origin_y, size)

    not_found_count = 0  

def draw_greater_than(origin_x, origin_y, size):
    pyautogui.mouseDown(origin_x, origin_y)
    pyautogui.moveTo(origin_x + size, origin_y + size, duration=draw_duration)
    pyautogui.moveTo(origin_x, origin_y + size, duration=draw_duration)
    pyautogui.mouseUp()

def draw_less_than(origin_x, origin_y, size):
    pyautogui.mouseDown(origin_x + size, origin_y)
    pyautogui.moveTo(origin_x, origin_y + size, duration=draw_duration)
    pyautogui.moveTo(origin_x + size, origin_y + size, duration=draw_duration)
    pyautogui.mouseUp()

def main():
    keyboard.add_hotkey('-', lambda: sys.exit("进程已结束"))

    try:
        while True:
            image = capture_area()
            numbers = recognize_numbers(image)
            nums = numbers
            draw_comparison(nums)
            time.sleep(0.35)  # 每次绘画及识别的延迟 不要改！
    except SystemExit as e:
        print(e)

if __name__ == "__main__":
    main()
