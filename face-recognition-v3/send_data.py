from kafka import KafkaProducer
from datetime import datetime
import os

def take_picture():
    picture_time = datetime.now()
    picture_location = f"{picture_time}.jpg".replace(' ', '')
    os.system(f"fswebcam -r 1280x730 --no-banner {picture_location}")
    return picture_location, picture_time

def delete_picture(picture_location):
    os.remove(picture_location)

def read_picture_data(picture_location):
    return open(picture_location, 'rb').read()

producer = KafkaProducer(
    bootstrap_servers=['0.tcp.au.ngrok.io:10753'])

picture_location, picture_time = take_picture()
# picture_time = datetime.now()
# picture_location='/Users/raf/projects/testing-face-recognition/face-recognition-v3/2019-06-30-201951_1184x624_scrot.png'
picture_data = read_picture_data(picture_location)

future = producer.send('picture', key=bytes(str(picture_time), 'utf-8'), value=picture_data)
producer.flush()