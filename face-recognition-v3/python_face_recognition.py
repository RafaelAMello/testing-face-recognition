import numpy as np
from PIL import ImageDraw, Image
import face_recognition

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
        return known_face_files[best_match_index], (0, 0, 255)
    else:
        return "Unknown", (255, 0, 0)

def draw_face(unknown_image):
    face_locations = face_recognition.face_locations(unknown_image, model="cnn")
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name, color = get_best_match(face_encoding, matches)
        draw.rectangle(((left, top), (right, bottom)), outline=color)
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=color, outline=color)
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
    del draw
    pil_image.show()

def process_face(file_name):
    unknown_image = face_recognition.load_image_file(file_name)
    draw_face(unknown_image)