import cv2
import requests

base_url = "http://192.168.42.99/"


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# pre-trained face detection model  
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    # Read frame
    ret, frame = cap.read()

    # Check if successfully captured
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # If a face is detected, send an HTTP request to turn on the LED
    if len(faces) > 0:
        url = base_url + "ledon"
    else:
        url = base_url + "ledoff"

    # Send the HTTP GET request
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Request sent successfully.")
        else:
            print(f"Failed to send request. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    # Display the frame
    cv2.imshow('Face Detection', frame)

    # exit loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()