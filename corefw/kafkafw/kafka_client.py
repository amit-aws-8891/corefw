import json

from flask import current_app
from kafka import KafkaConsumer, KafkaProducer

from corefw import get_settings


class KafkaClient(object):
    def __init__(self, topic_name, group_id=None):
        self.topic_name = topic_name
        self.kafka_servers = list(
            map(str.strip, get_settings(current_app, "KAFKA_SERVERS").split(","))
        )
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=self.kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        self.kafka_consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=self.kafka_servers,
            group_id=group_id,
            auto_offset_reset="earliest",
        )

    def send_json(self, data):
        """
        Producer - This will send json data to kafka
        """
        self.kafka_producer.send(self.topic_name, data)

    def get_data_from_consumer(self, topic_name):
        """
        Get data from kafka for specific topic
        """
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=self.kafka_servers,
            group_id=None,
            auto_offset_reset="smallest",
        )
        return consumer

    def get_kafka_consumer_instance(self):
        return self.kafka_consumer
