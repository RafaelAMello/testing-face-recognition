import io
import requests
from time import sleep
from requests.exceptions import ConnectionError
import json
from kafka import KafkaConsumer, KafkaProducer
from PIL import Image

consumer = KafkaConsumer(
            'picture',
            group_id='my-group',
            bootstrap_servers='kafka-49b7861-rafaelathaydemello-3b01.aivencloud.com:25697',
            security_protocol="SSL",
            ssl_cafile="ca.pem",
            ssl_certfile="service.cert",
            ssl_keyfile="service.key"
)

producer = KafkaProducer(
    bootstrap_servers='kafka-49b7861-rafaelathaydemello-3b01.aivencloud.com:25697',
    security_protocol="SSL",
    ssl_cafile="ca.pem",
    ssl_certfile="service.cert",
    ssl_keyfile="service.key",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def download_faces(process_function, send_kafka_payload=False):
    for message in consumer:
        print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key}")
        image = Image.open(io.BytesIO(message.value))
        file_name = "test.jpg"
        image.save(file_name)
        if send_kafka_payload:
            payload = process_function(file_name)
            picture_time = message.key
            producer.send('picture-metadata', key=picture_time, value=payload)
        else:
            process_function(file_name)

if __name__ == "__main__":
    wait_to_become_available = True
    while True:
        try:
            requests.get("http://127.0.0.1:8080")
            wait_to_become_available = False
        except ConnectionError:
            print("Machine learning Not available")
            sleep(1)
    from facebox_face_recognition import process_faces
    download_faces(process_faces, send_kafka_payload=True)