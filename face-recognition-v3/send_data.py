from kafka import KafkaProducer
from json import dumps

producer = KafkaProducer(bootstrap_servers=['0.tcp.au.ngrok.io:10624'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))


producer.send('picture', value={'hello' : 'world'})
