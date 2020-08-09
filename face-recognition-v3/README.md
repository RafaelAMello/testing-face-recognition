ssh -N -L 0.0.0.0:8888:localhost:8080 -N 127.0.0.1

ssh -C -N raf@127.0.0:9092 -L 9092:127.0.0.1:9092

~/ngrok tcp 9092

docker run -p 8080:8080 -e "MB_KEY=$MB_KEY" machinebox/facebox

docker run -p 8080:8080 -e "MB_KEY=$MB_KEY" machinebox/tagbox
