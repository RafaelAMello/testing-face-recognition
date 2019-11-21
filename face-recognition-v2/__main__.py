from google.cloud import pubsub_v1
import face_recognition
import glob
import os

def create_subscriber():
    project_id = "hotdoc-hubspot"
    topic_name = "raspberry-pi"
    subscription_name = "raf_computer"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    return subscriber, subscription_path

def parse_created_at(created_at):
    return created_at.split('/')[-1]

def process_pic(message):
    print('Received', message.attributes['created_at'])
    with open('pics/' + parse_created_at(message.attributes['created_at']), 'wb') as file:
        file.write(message.data)
    message.ack()

def face_map():
    pass

if __name__ == '__main__':
    subscriber, subscription_path = create_subscriber()
    subscriber.subscribe(subscription_path, process_pic)
    known_image = face_recognition.load_image_file("known_faces/rafael.jpg")
    raf_face = face_recognition.face_encodings(known_image)[0]
    while True:
        unknown_images = glob.glob('pics/*.jpg')
        for unknown_image_location in unknown_images:
            print("Scanning Photo", unknown_image_location)
            unknown_image = face_recognition.load_image_file(unknown_image_location)
            unknown_faces = face_recognition.face_encodings(unknown_image)
            if unknown_faces:
                print("Found Faces in", unknown_image_location)
                for face in unknown_faces:
                    results = face_recognition.compare_faces([raf_face], face)
                    print(results)
                    os.rename(unknown_image_location, 'recognized_faces/' + unknown_image_location.split('/')[-1])
            else:
                print("No Faces Found in", unknown_image_location)
                # os.remove(unknown_image_location)
