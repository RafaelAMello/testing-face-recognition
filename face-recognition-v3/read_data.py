from kafka import KafkaConsumer
import numpy as np
import io
from PIL import Image, ImageDraw
import face_recognition

consumer = KafkaConsumer(
                'picture',
                group_id='my-group',
                bootstrap_servers='kafka-49b7861-rafaelathaydemello-3b01.aivencloud.com:25697',
                security_protocol="SSL",
                ssl_cafile="ca.pem",
                ssl_certfile="service.cert",
                ssl_keyfile="service.key"
)


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
    face_locations = face_recognition.face_locations(unknown_image)
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

for message in consumer:
    print (f"{message.topic}:{message.partition}:{message.offset}: key={message.key}")
    image = Image.open(io.BytesIO(message.value))
    image.save('test.jpg')
    unknown_image = face_recognition.load_image_file("test.jpg")
    draw_face(unknown_image)
