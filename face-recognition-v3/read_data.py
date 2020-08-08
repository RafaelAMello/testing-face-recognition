from kafka import KafkaConsumer

consumer = KafkaConsumer('picture',
                         group_id='my-group',
                         bootstrap_servers=['0.tcp.au.ngrok.io:10504 '])


for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))