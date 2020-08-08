from kafka import KafkaConsumer

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
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s"
     % (message.topic, message.partition,
                                          message.offset, message.key))
                                          