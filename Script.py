import time
import cv2
import numpy as np
import pyautogui

# Настройки задержек (для реалистичности)
MOVE_DELAY = (0.1, 0.3)
E_PRESS_DELAY = (0.5, 1.2)
TURN_DELAY = (0.2, 0.5)

# Координаты карты на экране (подстрой под себя!)
MAP_REGION = (1600, 800, 300, 200)  # x, y, width, height

# Цвет красной метки (RGB)
RED_LOWER = np.array([150, 0, 0])
RED_UPPER = np.array([255, 80, 80])


def capture_screen(region=None):
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def find_red_marker():
    img = capture_screen(MAP_REGION)
    mask = cv2.inRange(img, RED_LOWER, RED_UPPER)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        return x + w // 2, y + h // 2
    return None


def turn_towards_marker(marker):
    screen_center_x = MAP_REGION[2] // 2
    marker_x = marker[0]
    if marker_x < screen_center_x - 20:
        print("↩️ Поворачиваем влево")
        pyautogui.keyDown('a')
        time.sleep(np.random.uniform(*TURN_DELAY))
        pyautogui.keyUp('a')
    elif marker_x > screen_center_x + 20:
        print("↪️ Поворачиваем вправо")
        pyautogui.keyDown('d')
        time.sleep(np.random.uniform(*TURN_DELAY))
        pyautogui.keyUp('d')


def move_character():
    while True:
        marker = find_red_marker()
        if marker:
            print("🟢 Метка найдена! Двигаемся...")
            turn_towards_marker(marker)
            pyautogui.keyDown('w')  # Бежать вперёд
            time.sleep(np.random.uniform(*MOVE_DELAY))
            pyautogui.keyUp('w')
        
        if detect_interact_prompt():
            print("🔵 Нажимаем E!")
            pyautogui.press('e')
            time.sleep(np.random.uniform(*E_PRESS_DELAY))

        time.sleep(0.5)


def detect_interact_prompt():
    screen = capture_screen()
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    if np.sum(thresh) > 500000:  # Если на экране есть светлая область
        return True
    return False


if __name__ == "__main__":
    print("🚀 Бот запущен! Ожидание 5 секунд...")
    time.sleep(5)
    move_character()
