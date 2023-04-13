import io
import time
import picamera
from PIL import Image
from pyzbar import pyzbar
import cv2
import RPi.GPIO as GPIO

# Inizializza la fotocamera
camera = picamera.PiCamera()

# Imposta la risoluzione della fotocamera
camera.resolution = (640, 480)

# Crea uno stream di immagini
stream = io.BytesIO()

# Imposta le dimensioni della finestra di visualizzazione
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', 800, 600)

# Imposta i pin GPIO della matrice della tastiera a membrana
MATRIX = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#", "D"]
]
ROW = [6, 13, 19, 26]
COL = [12, 16, 20, 21]

GPIO.setwarnings(False)

# Imposta i pin GPIO in modalità BCM
GPIO.setmode(GPIO.BCM)

video_files = {
#videospath   
}

# Imposta i pin GPIO delle righe come output e le colonne come input
for j in range(4):
    GPIO.setup(COL[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
for i in range(4):
    GPIO.setup(ROW[i], GPIO.OUT)


def capture_image():
    # Cattura un'immagine dal sensore della fotocamera
    camera.capture(stream, format='jpeg', use_video_port=True)

    # Torna all'inizio dello stream per la lettura
    stream.seek(0)

    # Carica l'immagine dallo stream in una PIL image
    pil_image = Image.open(stream)

    return pil_image


def play_video(video_file):
    cap = cv2.VideoCapture(video_file)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


def read_keypad():
    for i in range(4):
        GPIO.output(ROW[i], 0)
        for j in range(4):
            if GPIO.input(COL[j]) == 0:
                key = MATRIX[i][j]
                time.sleep(0.2)
                GPIO.output(ROW[i], 1)
                return key
        GPIO.output(ROW[i], 1)
    return None


def main_loop():
    while True:
        pil_image = capture_image()

        # Utilizza pyzbar per trovare e decodificare il codice QR
        qr_codes = pyzbar.decode(pil_image)

        # Cicla attraverso i codici QR trovati nell'immagine
        for qr_code in qr_codes:
            qr_releved = qr_code.data.decode()
            print(qr_releved)
            if qr_decoded == "": #qrcode
                print("Please, select a video")

                while True:
                    key = read_keypad()
                    if key in video_files:
                        play_video(video_files[key])

        # Resetta lo stream per la prossima immagine
        stream.seek(0)
        stream.truncate()


if __name__ == "__main__":
    main_loop()
