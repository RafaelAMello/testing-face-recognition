import face_recognition
import cv2
import glob
from datetime import datetime

video_capture = cv2.VideoCapture(0)
encoding = {}

def encode_users(known_images_dir='./known_images/*.png'):
    for person in glob.glob(known_images_dir):
        encoding[person] = face_recognition.face_encodings(face_recognition.load_image_file(person))[0]
    return encoding


encodings = encode_users()


def grab_frame(video_capture):
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    return rgb_small_frame, frame

def process_frame(rgb_small_frame):
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face in face_encodings:
        matches = face_recognition.compare_faces(list(encoding.values()), face)
        
        if True in matches:
            first_match_index = matches.index(True)
            name = list(encoding.keys())[first_match_index]

        else:
            name = "unknown"

        face_names.append(name)
    
    return face_locations, face_names

def draw_boxes(face_locations, face_names, frame):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        if name == 'unknown':
            colour = (0, 0, 255)
        else:
            colour = (0, 128, 0)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), colour, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), colour, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


while True:
    rgb_small_frame, frame = grab_frame(video_capture)
    face_locations, face_names = process_frame(rgb_small_frame)
    draw_boxes(face_locations, face_names, frame)
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
