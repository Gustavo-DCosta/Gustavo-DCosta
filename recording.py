import cv2
import os
import pyaudio
import wave
import keyboard
import time
import threading

def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    
    while os.path.exists(unique_filename):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1
    
    return unique_filename

def record_video():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = cap.read()
    if ret:
        print("Captured frame resolution:", frame.shape)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame.shape[1])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame.shape[0])

    # Get a unique filename for video
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
            print(f"Video recording: {recording}")

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

def record_audio():
    chunk = 1024
    format = pyaudio.paInt16
    channels = 2
    rate = 44100

    # Get a unique filename for audio
    output_file = get_unique_filename("recorded_audio.wav")

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk) 

    frames = []
    print("Press SPACE to start audio recording")
    keyboard.wait('space')
    print("Audio recording... Press SPACE to stop.")
    time.sleep(0.2)  

    while True:
        data = stream.read(chunk)  
        frames.append(data)
        if keyboard.is_pressed('space'):
            print("Stopping audio recording") 
            time.sleep(0.2)
            break   

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_file, 'wb')  
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()  # Finalize the WAV file

# Create threads for simultaneous video and audio recording
video_thread = threading.Thread(target=record_video)
audio_thread = threading.Thread(target=record_audio)

# Start both threads
video_thread.start()
audio_thread.start()

# Wait for both threads to complete
video_thread.join()
audio_thread.join()
