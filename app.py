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
        r.delete('conn_url')
        r.set('connection_requested', 'yes')
        while r.get('conn_url') is None:
            pass
        return jsonify({'conn_url' : r.get('conn_url').decode()})
    return password

@app.route('/<password>', methods=['DELETE'])
def delete_con(password):
    if PASSWORD == password:
        if r.get('conn_url') is None:
            return jsonify({'done' : False})
        r.set('connection_delete_requested', 'yes')
        while r.get('conn_url') is not None:
            pass
        return jsonify({'done' : True})
    return password

if __name__ == "__main__":
    app.run()