import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np

SMOOTHING = 5
CLICK_DIST = 30
FRAME_REDUCTION = 100
CAM_WIDTH, CAM_HEIGHT = 640, 480

class HandController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_positions(self, img):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]
            h, w, c = img.shape
            for id, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

    def fingers_up(self, lm_list):
        fingers = []
        if lm_list[4][1] < lm_list[3][1]: 
            fingers.append(1)
        else:
            fingers.append(0)

        for id in [8, 12, 16, 20]:
            if lm_list[id][2] < lm_list[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

def draw_centered_text(img, text, y_pos, size=1.0, color=(255, 255, 255), thickness=2):
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, size, thickness)[0]
    text_x = (img.shape[1] - text_size[0]) // 2
    cv2.putText(img, text, (text_x, y_pos), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)
    
    detector = HandController()
    state = "MENU"

    while True:
        success, img = cap.read()
        if not success: break

        img = cv2.flip(img, 1)
        img = detector.find_hands(img, draw=(state == "PLAYING")) 
        lm_list = detector.get_positions(img)
        
        fingers = []
        if len(lm_list) != 0:
            fingers = detector.fingers_up(lm_list)

        if state == "MENU":
            img = cv2.GaussianBlur(img, (51, 51), 0)
            
            overlay = img.copy()
            cv2.rectangle(overlay, (0, 0), (CAM_WIDTH, CAM_HEIGHT), (0, 0, 0), -1)
            img = cv2.addWeighted(overlay, 0.4, img, 0.6, 0)

            draw_centered_text(img, "CONTROLE GESTUAL", 150, 1.5, (0, 255, 255), 3)
            draw_centered_text(img, "Gesto: Paz e Amor (V) para Iniciar", 250, 0.7)
            draw_centered_text(img, "Ou pressione [ESPACO]", 290, 0.6, (200, 200, 200), 1)
            draw_centered_text(img, "[Q] para Sair do Programa", 450, 0.6, (100, 100, 255), 1)

            if len(fingers) == 5:
                if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    state = "PLAYING"

        elif state == "PLAYING":
            cv2.rectangle(img, (FRAME_REDUCTION, FRAME_REDUCTION), 
                         (CAM_WIDTH - FRAME_REDUCTION, CAM_HEIGHT - FRAME_REDUCTION),
                         (255, 0, 255), 2)
            
            cv2.putText(img, "Modo: JOGO (Tecle 'M' para Menu)", (10, 30), 
                       cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

            if len(lm_list) != 0:
                x1, y1 = lm_list[8][1], lm_list[8][2]
                x2, y2 = lm_list[4][1], lm_list[4][2]

                if fingers[1] == 1 and fingers[2] == 0:
                    x3 = np.interp(x1, (FRAME_REDUCTION, CAM_WIDTH - FRAME_REDUCTION), (0, detector.screen_w))
                    y3 = np.interp(y1, (FRAME_REDUCTION, CAM_HEIGHT - FRAME_REDUCTION), (0, detector.screen_h))

                    detector.curr_x = detector.prev_x + (x3 - detector.prev_x) / SMOOTHING
                    detector.curr_y = detector.prev_y + (y3 - detector.prev_y) / SMOOTHING

                    pyautogui.moveTo(detector.curr_x, detector.curr_y)
                    detector.prev_x, detector.prev_y = detector.curr_x, detector.curr_y

                    distance = math.hypot(x2 - x1, y2 - y1)
                    if distance < CLICK_DIST:
                        cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()
                
                if sum(fingers) == 5:
                    cv2.putText(img, "ACELERA (W)", (50, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                elif sum(fingers) == 0:
                    cv2.putText(img, "FREIA (S)", (50, 400), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == 32 and state == "MENU":
            state = "PLAYING"
        if key == ord('m') and state == "PLAYING":
            state = "MENU"

        cv2.imshow("Gestures Pro V2", img)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()