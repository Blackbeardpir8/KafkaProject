from confluent_kafka import Producer
import json
import time

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(**conf)

start_latitude = 21.2514
start_longitude = 81.6296

end_latitude = 21.1904
end_longitude = 81.2849

number_steps = 1000
step_size_lat = (end_latitude - start_latitude) / number_steps
step_size_lon = (end_longitude - start_longitude) / number_steps
current_steps = 0

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

topic = "location_updates"
while True:
    latitude = start_latitude + step_size_lat * current_steps
    longitude = start_longitude + step_size_lon * current_steps

    data = {
        "latitude": latitude,
        "longitude": longitude,
    }

    print(data)

    producer.produce(topic, json.dumps(data).encode('utf-8'), callback=delivery_report)
    producer.flush()

    current_steps += 1
    if current_steps > number_steps:
        current_steps = 0

    time.sleep(2)
