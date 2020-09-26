import os
from flask import Flask
from flask import jsonify
import redis

app = Flask(__name__)
PASSWORD =  os.environ['PASSWORD']
r = redis.from_url(os.environ['REDIS_URL'])

@app.route('/<password>', methods=['GET'])
def get_con(password):
    if PASSWORD == password:
        r.set('connection_requested', 'True')
        while r.get('connection_requested') is not None and r.get('connection_requested').decode() == 'False':
            pass
        data = {
            'ssh_conn_url' : r.get('ssh_conn_url').decode(),
            'vnc_conn_url' : r.get('vnc_conn_url').decode()
        }
        return jsonify(data)
    return password

@app.route('/<password>', methods=['DELETE'])
def delete_con(password):
    if PASSWORD == password:
        r.set('connection_delete_requested', 'True')
        while r.get('connection_delete_requested') is not None and r.get('connection_delete_requested').decode() == 'True':
            pass
        return jsonify({'done' : True})
    return password

if __name__ == "__main__":
    app.run()