from json import dumps
from kafka import KafkaProducer
from kafka import KafkaAdminClient
from kafka import KafkaConsumer
from json import loads
from kafka.errors import UnknownTopicOrPartitionError
import time

admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'])

def delete_topics(*arg):
    try:
        admin_client.delete_topics(topics=[*arg])
        print("Topic Deleted Successfully")
    except UnknownTopicOrPartitionError as e:
        print("Topic Doesn't Exist")
    except  Exception as e:
        print(e)

delete_topics('numtest')

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


for e in range(4):
    data = {'number' : e}
    producer.send('numtest', value=data)
    time.sleep(0.01)


consumer = KafkaConsumer(
    'numtest',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))




for message in consumer:
    message = message.value
    print(message)