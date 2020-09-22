import os
import redis
from time import sleep
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv('.env')
r = redis.from_url(os.environ['REDIS_URL'])

def delete_connections(r):
    ngrok.kill()
    r.delete('ssh_conn_url')
    r.delete('vnc_conn_url')
    r.delete('connection_requested')
    r.delete('connection_delete_requested')

try:
    while True:
        if r.get('connection_delete_requested') is not None:
            print("Handling Delete")
            delete_connections(r)

        if r.get('connection_requested') is not None:
            delete_connections(r)
            print("Handling Create")
            r.set('ssh_conn_url', ngrok.connect(22, "tcp"))
            r.set('vnc_conn_url', ngrok.connect(5900, "tcp"))
            r.delete('connection_requested')

except KeyboardInterrupt as err:
    print()
    print("Terminating")
    ngrok.kill()
    r.delete('conn_url')
    r.delete('connection_delete_requested')
    r.delete('connection_requested')