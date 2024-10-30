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

# Fungsi untuk menghitung jumlah jari yang terangkat
def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Indeks landmark ujung jari (telunjuk - kelingking)
    thumb_tip = 4  # Indeks ujung ibu jari
    count = 0

    # Ibu jari (thumb): posisinya berbeda dari jari lain
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 2].x:
        count += 1

    # Hitung jari telunjuk hingga kelingking
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1

    return count

# Fungsi untuk mengirim perintah melalui HTTP
async def send_command(command):
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}?State={command}"
        async with session.get(url) as response:
            if response.status == 200:
                print(f"Command {command} sent successfully.")
            else:
                print(f"Failed to send command {command}.")

# Fungsi utama untuk menangkap video dan mengirim perintah
async def main():
    cap = cv2.VideoCapture(0)  # Gunakan kamera

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Konversi frame ke RGB untuk MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Hitung jumlah jari yang terangkat
                finger_count = count_fingers(hand_landmarks)

                # # Kirim perintah sesuai jumlah jari yang terangkat
                # if finger_count == 1:
                #     await send_command("F")  # Maju
                # elif finger_count == 2:
                #     await send_command("B")  # Mundur
                # elif finger_count == 3:
                #     await send_command("R")  # Belok kiri
                # elif finger_count == 4:
                #     await send_command("L")  # Belok kanan
                # elif finger_count == 0:
                #     await send_command("S")  # Stop

                if finger_count == 2:
                    await send_command("F")  # Maju
                elif finger_count == 3:
                    await send_command("B")  # Mundur
                elif finger_count == 4:
                    await send_command("R")  # Belok kiri
                elif finger_count == 5:
                    await send_command("L")  # Belok kanan
                elif finger_count == 1:
                    await send_command("S")  # Stop

        # Tampilkan frame dengan deteksi tangan
        cv2.imshow("Hand Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    await send_command("S")

# Jalankan program
if __name__ == "__main__":
    asyncio.run(main())
