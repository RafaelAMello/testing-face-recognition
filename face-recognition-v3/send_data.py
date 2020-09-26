from dotenv import load_dotenv
from kafka import KafkaProducer

from .take_pic import take_picture

load_dotenv('.env')

BOOTSTRAP_SERVER = f"{os.getenv('KAFKA_SERVER_HOST')}:{os.getenv('KAFKA_SERVER_PORT')}"

def delete_picture(picture_location):
    os.remove(picture_location)

def read_picture_data(picture_location):
    return open(picture_location, 'rb').read()

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVER,
)

while True:
    print("Taking Picture")
    picture_location, picture_time = take_picture()
    print("Reading Picture")
    picture_data = read_picture_data(picture_location)
    print("Sending Picture")
    future = producer.send('picture', key=bytes(str(picture_time), 'utf-8'), value=picture_data)
    delete_picture(picture_location)