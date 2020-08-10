FROM python:slim

WORKDIR /home
COPY . ./

RUN pip install kafka-python
RUN pip install Pillow
RUN pip install requests

CMD python read_data.py