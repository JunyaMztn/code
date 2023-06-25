import pyautogui

pos_x, pos_y = pyautogui.position()
#print("現在のマウスカーソル位置 X：", pos_x)
#print("現在のマウスカーソル位置 Y：", pos_y)
print('(X, Y) = (' + str(pos_x) + ', ' + str(pos_y) + ')')