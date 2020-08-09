import io
from kafka import KafkaConsumer
from PIL import Image

def download_faces(process_function):
    consumer = KafkaConsumer(
                'picture',
                group_id='my-group',
                bootstrap_servers='kafka-49b7861-rafaelathaydemello-3b01.aivencloud.com:25697',
                security_protocol="SSL",
                ssl_cafile="ca.pem",
                ssl_certfile="service.cert",
                ssl_keyfile="service.key"
    )
    for message in consumer:
        print(f"{message.topic}:{message.partition}:{message.offset}: key={message.key}")
        image = Image.open(io.BytesIO(message.value))
        file_name = "test.jpg"
        image.save(file_name)
        process_function(file_name)

if __name__ == "__main__":
    # from python_face_recognition import process_face
    # download_faces(process_face)