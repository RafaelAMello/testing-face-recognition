import os
import redis
from time import sleep
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv('.env')
r = redis.from_url(os.environ['REDIS_URL'])
try:
    while True:
        if r.get('connection_delete_requested') is not None:
            print("Handling Delete")
            ngrok.kill()
            r.delete('conn_url')
            r.delete('connection_delete_requested')

        if r.get('connection_requested') is not None:
            ngrok.kill()
            print("Handling Create")
            ssh_url = ngrok.connect(22, "tcp")
            r.set('conn_url', ssh_url)
            r.delete('connection_requested')

except KeyboardInterrupt as err:
    print()
    print("Terminating")
    ngrok.kill()
    r.delete('conn_url')
    r.delete('connection_delete_requested')
    r.delete('connection_requested')