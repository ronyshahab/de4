import os
import threading
import cv2
from deepface import DeepFace

uploadsDir= "./uploads"
isRunning = False
model_name = "Facenet"
model = DeepFace.build_model(model_name)
detector_backend = "opencv"


def face_verify():
    global isRunning
    if isRunning:
        print("Face verification already running.")
        return

    isRunning = True
    image_files = [f for f in os.listdir(uploadsDir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".heic", ".dng"))]

    if not image_files:
        print("No images found in uploads/")
        isRunning = False
        return
    
    reference_images = [cv2.imread(os.path.join(uploadsDir, img)) for img in image_files]

    reference_images = [img for img in reference_images if img is not None]

    if not reference_images:
        print("No valid images loaded.")
        isRunning = False
        return
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    counter = 0
    face_match = False

    def check_face(frame):
        nonlocal face_match
        for ref in reference_images:
            try:
                result = DeepFace.verify(
                    frame,
                    ref.copy(),
                    model_name=model_name,
                    model=model,
                    detector_backend=detector_backend,
                    enforce_detection=False
                )
                if result["verified"]:
                    face_match = True
                    break
            except:
                continue
    while isRunning:
        ret, frame = cap.read()

        if ret:
            if counter % 30 == 0:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            counter += 1

            text = "MATCH!" if face_match else "NO MATCH!"
            color = (0, 255, 0) if face_match else (0, 0, 255)
            cv2.putText(frame, text, (20, 450), cv2.FONT_HERSHEY_COMPLEX, 2, color, 3)

            cv2.imshow("video", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    isRunning=False

def stop_verification():
    global verification_running
    verification_running = False
    print("Verification stopped.")
