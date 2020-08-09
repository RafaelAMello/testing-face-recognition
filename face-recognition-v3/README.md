ssh -N -L 0.0.0.0:8888:localhost:8080 -N 127.0.0.1

ssh -C -N raf@127.0.0:9092 -L 9092:127.0.0.1:9092


docker run -p 8080:8080 -e "MB_KEY=$MB_KEY" machinebox/facebox
python read_data.py
docker run -p 8888:8888 -v $(pwd):/home/jovyan/local  -e GRANT_SUDO=yes --user root jupyter/pyspark-notebook


openssl pkcs12 -export -inkey service.key -in service.cert -out client.keystore.p12 -name service_key
keytool -import -file ca.pem -alias CA -keystore client.truststore.jks