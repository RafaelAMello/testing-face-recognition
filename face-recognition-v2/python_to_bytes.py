
import argparse
import sys
from google.cloud import pubsub_v1

parser = argparse.ArgumentParser(description='Read a pic into bytes')
parser.add_argument('--name', help='image name')
args = parser.parse_args()

project_id = 'hotdoc-hubspot'
topic_name = 'raspberry-pi'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

with open(args.name, "rb") as image:
      f = image.read()
      publisher.publish(topic_path, bytes(f), created_at=args.name)
