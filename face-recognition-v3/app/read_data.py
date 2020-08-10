import io
import requests
from time import sleep
from requests.exceptions import ConnectionError
import json
from kafka import KafkaConsumer, KafkaProducer
from PIL import Image
from facebox_face_recognition import process_faces, train_faces

consumer = KafkaConsumer(
            'picture',
            group_id='my-group',
            bootstrap_servers='kafka-49b7861-rafaelathaydemello-3b01.aivencloud.com:25697',
            security_protocol="SSL",
            ssl_cafile="keys/ca.pem",
            ssl_certfile="keys/service.cert",
            ssl_keyfile="keys/service.key"
)

producer = KafkaProducer(
    bootstrap_servers='kafka-49b7861-rafaelathaydemello-3b01.aivencloud.com:25697',
    security_protocol="SSL",
    ssl_cafile="keys/ca.pem",
    ssl_certfile="keys/service.cert",
    ssl_keyfile="keys/service.key",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def download_faces(process_function, send_kafka_payload=False):
    for message in consumer:
        print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key}")
        image = Image.open(io.BytesIO(message.value))
        file_name = "test.jpg"
        image.save(file_name)
        picture_time = message.key
        if send_kafka_payload:
            payload = process_function(file_name, picture_time)
            producer.send('picture-metadata', key=picture_time, value=payload)
        else:
            process_function(file_name)

if __name__ == "__main__":
    print("Checking availability of model")
    wait_to_become_available = True
    while wait_to_become_available:
        try:
            requests.get("http://facerecognition:8080")
            wait_to_become_available = False
        except ConnectionError:
            print("Machine learning Not available")
            sleep(1)
    train_faces()
    download_faces(process_faces, send_kafka_payload=True)