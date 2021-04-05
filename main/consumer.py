# amqps://jniebliu:zUYztH2N6gHQ2q47IWdeWDjyVZBS1DB4@hornet.rmq.cloudamqp.com/jniebliu

import pika, json
from main import Product, db

params = pika.URLParameters('amqps://jniebliu:zUYztH2N6gHQ2q47IWdeWDjyVZBS1DB4@hornet.rmq.cloudamqp.com/jniebliu')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], tittle=data['tittle'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('product created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.tittle = data['tittle']
        product.image = data['image']
        db.session.commit()
        print('product updated')
    
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('product deleted')

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Hi Camila started consuming')

channel.start_consuming()

channel.close()