import os
from datetime import datetime

from dotenv import load_dotenv
from kafka import KafkaProducer

load_dotenv(dotenv_path)

BOOTSTRAP_SERVER = f"{os.getenv('KAFKA_SERVER_HOST')}:{os.getenv('KAFKA_SERVER_PORT')}"

def take_picture():
    picture_time = datetime.now()
    picture_location = f"{picture_time}.jpg".replace(' ', '')
    # https://lbhtran.github.io/Camera-setting-and-photo-taking-schedule-to-get-the-best-result/
    # fswebcam -D 2 -S 20 --set Focus, Auto=False --set brightness=30% --set contrast=0%  -F 10 -r  640x480 --no-banner /home/pi/camera/$DATE.jpg
    os.system(f'fswebcam -S 20 -r 1280x730 --set "Zoom, Absolute"=500 --no-banner {picture_location}')
    return picture_location, picture_time

def delete_picture(picture_location):
    os.remove(picture_location)

def read_picture_data(picture_location):
    return open(picture_location, 'rb').read()

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
    security_protocol="SSL",
    ssl_cafile="keys/ca.pem",
    ssl_certfile="keys/service.cert",
    ssl_keyfile="keys/service.key"
)

while True:
    print("Taking Picture")
    picture_location, picture_time = take_picture()
    print("Reading Picture")
    picture_data = read_picture_data(picture_location)
    print("Sending Picture")
    future = producer.send('picture', key=bytes(str(picture_time), 'utf-8'), value=picture_data)
    delete_picture(picture_location)