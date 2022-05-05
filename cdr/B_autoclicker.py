import keyboard, pyautogui as m, mouse

while True:
    if keyboard.is_pressed('alt'):
        m.click(button='right')
        m.move(15,15)
        m.click()
    if keyboard.is_pressed('shift'):
        m.moveTo(1627, 394)
        m.click()
        m.moveTo(175,614)