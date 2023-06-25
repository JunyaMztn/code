import pyautogui

# 座標指定
START_X = 400
START_Y = 300
END_X = 600
END_Y = 800

pyautogui.moveTo(START_X, START_Y)

pyautogui.dragTo(END_X, END_Y, duration=2, button="left")