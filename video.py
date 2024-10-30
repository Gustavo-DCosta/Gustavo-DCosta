import cv2
import os

def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    
    while os.path.exists(unique_filename):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1
    
    return unique_filename

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ret, frame = cap.read()
if ret:
    print("Captured frame resolution:", frame.shape)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame.shape[1])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame.shape[0])

# Get a unique filename to prevent overwriting
output_file = get_unique_filename("recording.avi")
fourcc = cv2.VideoWriter_fourcc(*'XVID')
writer = cv2.VideoWriter(output_file, fourcc, 30.0, (frame.shape[1], frame.shape[0]))

recording = False

while True:
    ret, frame = cap.read()

    if ret:
        cv2.imshow("video", frame)
        if recording:
            writer.write(frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):
        recording = not recording
        print(f"recording: {recording}")

cap.release()
writer.release()
cv2.destroyAllWindows()
