import numpy as np
import face_recognition
from draw_face import draw_face, initialize_draw, show_draw, BLUE, RED
known_face_files = [
    'rafael.jpg'
]
known_face_encodings = []
for file_path in known_face_files:
    image = face_recognition.load_image_file(file_path)
    face = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face)

def get_best_match(face_encoding, matches):
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        return known_face_files[best_match_index], BLUE
    else:
        return "Unknown", RED

def draw_faces(unknown_image):
    face_locations = face_recognition.face_locations(unknown_image, model="cnn")
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    draw, pil_image = initialize_draw(image=unknown_image)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name, color = get_best_match(face_encoding, matches)
        draw_face(draw, name, color, top, right, bottom, left)
    show_draw(draw, pil_image)

def process_face(file_name):
    unknown_image = face_recognition.load_image_file(file_name)
    draw_faces(unknown_image)