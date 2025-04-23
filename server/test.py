import os
import threading
import cv2
from deepface import DeepFace

uploadsDir = "./uploads"
isRunning = False
model_name = "VGG-Face"
model = DeepFace.build_model(model_name)
detector_backend = "opencv"
face_match = False
lock = threading.Lock()
verify_thread = None

def analyze_face(frame):
    try:
        result = DeepFace.analyze(frame, actions=["age", "gender"], enforce_detection=False)
        return True  
    except Exception as e:
        print(f"Face detection failed: {e}")
        return False 

def verify_faces_thread(frame, reference_images):
    global face_match

    if not analyze_face(frame):  
        return
    for ref in reference_images:
        try:
            result = DeepFace.verify(
                frame,
                ref,
                model_name=model_name,
                detector_backend=detector_backend,
                enforce_detection=False
            )
            if result["verified"]:
                with lock:
                    face_match = True
                print("face found")
                break
        except Exception as e:
            print("Verification error:", e)
            cv2.imshow("Bad Frame", frame)
            cv2.waitKey(1)

def face_verify():
    global isRunning, face_match, verify_thread
    if isRunning:
        print("Face verification already running.")
        return

    isRunning = True
    image_files = [f for f in os.listdir(uploadsDir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".heic", ".dng"))]

    if not image_files:
        print("No images found in uploads/")
        isRunning = False
        return

    reference_images = []
    for img_file in image_files:
        img_path = os.path.join(uploadsDir, img_file)
        img = cv2.imread(img_path)
        if img is not None:
            reference_images.append(img)

    if not reference_images:
        print("No valid images loaded.")
        isRunning = False
        return

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    counter = 0

    while isRunning:
        ret, frame = cap.read()
        if not ret:
            continue

        if counter % 30 == 0:
            if verify_thread is None or not verify_thread.is_alive():
                face_match = False
                verify_thread = threading.Thread(target=verify_faces_thread, args=(frame.copy(), reference_images))
                verify_thread.start()

        text = "MATCH!" if face_match else "NO MATCH!"
        color = (0, 255, 0) if face_match else (0, 0, 255)
        cv2.putText(frame, text, (20, 450), cv2.FONT_HERSHEY_COMPLEX, 2, color, 3)
        cv2.imshow("video", frame)

        key = cv2.waitKey(1)
        if key == ord("q"):
            print("Exiting...")
            break

        counter += 1

    cap.release()
    cv2.destroyAllWindows()
    isRunning = False

def stop_verification():
    global isRunning
    isRunning = False
    print("Verification stopped.")
