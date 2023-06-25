import pyautogui
import time

# 座標指定
START_X = 400   # 開始座標（X）
START_Y = 300   # 開始座標（Y）
END_X = 600     # 終了座標（X）
END_Y = 800     # 終了座標（Y）

# 時間指定 [sec]
S_TIME = 0.1    # 待ち時間
D_TIME = 0.5    # ドラッグの移動

# 現在のカーソル位置を取得
pos_x, pos_y = pyautogui.position()

# PrintScreen
pyautogui.hotkey("win", "shift", "s")

# 待ち時間
time.sleep(S_TIME)

# 開始位置の指定
pyautogui.moveTo(START_X, START_Y)

# 待ち時間
time.sleep(S_TIME)

# 終了位置までドラッグ（左クリック）
pyautogui.dragTo(END_X, END_Y, duration=D_TIME, button="left")

# 元のカーソル位置に戻る
pyautogui.moveTo(pos_x, pos_y)