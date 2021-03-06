from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

import os
import requests
import time

BROKER = os.environ['BROKER']
SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']

#print(BROKER)
#print(SCHEMA_REGISTRY_URL)

# sleep to give the schema-registry time to connect to kafka 
for i in range(120):
  print("I am sleeping for {} seconds".format(i))
  time.sleep(1)
print("I am done sleeping")

r = requests.get(SCHEMA_REGISTRY_URL + '/subjects/')
print("got my status code back! it's {}".format(r.status_code))
while r.status_code != 200:
    print("status code: {}. retrying...".format(r.status_code))
    r = requests.get(SCHEMA_REGISTRY_URL + '/subjects/')

value_schema = avro.loads("""
    {
        "namespace": "confluent.io.examples.serialization.avro",
        "name": "User",
        "type": "record",
        "fields": [
            {"name": "lat", "type": "float", "doc": "latitude"},
            {"name": "lng", "type": "float", "doc": "longitude"}
        ]
    }
""")

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

avroProducer = AvroProducer({
    'bootstrap.servers': BROKER,
    'on_delivery': delivery_report,
    'schema.registry.url': SCHEMA_REGISTRY_URL 
    }, default_value_schema=value_schema)

lat = 40.043152
lng = -75.18071

while True:
  for i in range(5):
    value = {
      "lat": lat,
      "lng": lng 
    }
    avroProducer.produce(topic='bus.locations', value=value)
    print("I just produced lat: {}, lng: {}".format(lat, lng))
    lat += 0.000001
    lng += 0.000001
  avroProducer.flush()
  print("I have flushed")
  time.sleep(5)

#record_schema_str = avro.loads("""
#{
#   "namespace": "septa.bus.location",
#   "name": "Location",
#   "type": "record",
#   "fields" : [
#     {
#       "name" : "lat",
#       "type" : "float",
#       "doc" : "latitude"
#     },
#     {
#       "name" : "lng",
#       "type" : "float",
#       "doc" : "longitude"
#     },
#     {
#       "name" : "direction",
#       "type" : "string",
#       "doc" : "the direction the bus is traveling",
#     },
#     {
#       "name" : "route",
#       "type" : "integer"
#       "doc" : "the bus route"
#     }
#   ]
#}
#""")

#key_schema_str = """
#{
#   "namespace": "septa.bus.location",
#   "name": "key",
#   "type": "record",
#   "fields" : [
#     {
#       "name" : "trip",
#       "type" : "integer"
#     }
#   ]
#}
#"""
#
#
#value_schema = avro.loads(value_schema_str)
#value = {
#  "lat": 40.043152,
#  "lng": -75.18071,
#  "direction": "NorthBound",
#  "route": 47
#}
#key = {"trip": 44802985}
#
#value = {
#  "lat": 40.043152,
#  "lng": -75.18071
#}