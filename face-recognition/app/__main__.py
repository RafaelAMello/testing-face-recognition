import face_recognition
import cv2
import glob
from datetime import datetime

video_capture = cv2.VideoCapture(0)
encoding = {}

for person in glob.glob('./known_images/*.png'):
    encoding[person] = face_recognition.face_encodings(face_recognition.load_image_file(person))[0]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face in face_encodings:
            matches = face_recognition.compare_faces(list(encoding.values()), face)
            
            if False not in matches:
                first_match_index = matches.index(True)
                name = list(encoding.keys())[first_match_index]

            else:
                name = "unknown"
                img_name = "unknown_image.png"
                # cv2.imwrite(img_name, frame)

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        if name == 'unknown':
            colour = (0, 0, 255)
        else:
            colour = (255, 0, 0)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), colour, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), colour, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
