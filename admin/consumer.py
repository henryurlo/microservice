# amqps://jniebliu:zUYztH2N6gHQ2q47IWdeWDjyVZBS1DB4@hornet.rmq.cloudamqp.com/jniebliu

import pika, json, os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from products.models import Product

params = pika.URLParameters('amqps://jniebliu:zUYztH2N6gHQ2q47IWdeWDjyVZBS1DB4@hornet.rmq.cloudamqp.com/jniebliu')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    print('Product likes increased')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Hi Camila started consuming')

channel.start_consuming()

channel.close()