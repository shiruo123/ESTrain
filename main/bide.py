# 导入相关库
import pyautogui
import random
import time


def no_xipin():
    # 使用while True循环，让程序一直执行！
    while True:
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        pyautogui.moveRel(x, y)
        time.sleep(270)  # 让鼠标移动到某个位置，停留几秒钟