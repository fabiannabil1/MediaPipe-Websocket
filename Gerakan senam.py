import cv2
import mediapipe as mp
import asyncio
import aiohttp

# Inisialisasi MediaPipe untuk deteksi tangan
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7)

# Alamat server untuk mengirim perintah
BASE_URL = "http://192.168.4.1/"

async def send_command(command):
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}?State={command}"
        async with session.get(url) as response:
            if response.status == 200:
                print(f"Command {command} sent successfully.")
            else:
                print(f"Failed to send command {command}.")

def is_hand_above(hand_landmarks):
    return hand_landmarks.landmark[0].y < 0.3

def hands_wide_apart(hand_landmarks1, hand_landmarks2):
    return abs(hand_landmarks1.landmark[0].x - hand_landmarks2.landmark[0].x) > 0.6

async def main():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        # Mendapatkan ukuran frame
        height, width, _ = frame.shape

        # Menambahkan garis pembatas kuadran
        cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 255, 0), 2)  # Garis vertikal
        cv2.line(frame, (0, height // 2), (width, height // 2), (0, 255, 0), 2)  # Garis horizontal

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            if len(result.multi_hand_landmarks) == 2:
                hand_landmarks1, hand_landmarks2 = result.multi_hand_landmarks

                if hands_wide_apart(hand_landmarks1, hand_landmarks2):
                    await send_command("B")
                
            elif len(result.multi_hand_landmarks) == 1:
                hand_landmarks = result.multi_hand_landmarks[0]
                if is_hand_above(hand_landmarks):
                    await send_command("F")
                elif hand_landmarks.landmark[0].x > 0.6:
                    await send_command("L")
                elif hand_landmarks.landmark[0].x < 0.4:
                    await send_command("R")
                else:
                    await send_command("S")  # Stop
        else:
            await send_command("S")

        # Gambar landmarks tangan pada frame
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    await send_command("S")

if __name__ == "__main__":
    asyncio.run(main())
