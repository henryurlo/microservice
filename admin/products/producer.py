# amqps://jniebliu:zUYztH2N6gHQ2q47IWdeWDjyVZBS1DB4@hornet.rmq.cloudamqp.com/jniebliu

import pika, json

params = pika.URLParameters('amqps://jniebliu:zUYztH2N6gHQ2q47IWdeWDjyVZBS1DB4@hornet.rmq.cloudamqp.com/jniebliu')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)