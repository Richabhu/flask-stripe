import stripe
from flask import Flask, jsonify, render_template, request, Response
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

stripe_keys = {
    'secret_key': os.environ['STRIPE_SECRET_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])


@app.route('/hello')
def hello_world():
    return jsonify('hello, world!')


@app.route('/checkout', methods=['POST'])
def charge():
    try:
        # amount in cents
        amount = 100
        print("kkk")
        #
        # customer = stripe.Customer.create(
        #     name='Jenny Rosen',
        #     address={t
        #         'line1': '510 Townsend St',
        #         'postal_code': '98140',
        #         'city': 'San Francisco',
        #         'state': 'CA',
        #         'country': 'US',
        #     },
        # )
        #
        # stripe.Charge.create(
        #     customer=customer.id,
        #     amount=amount,
        #     currency='usd',
        #     description='Flask Charge'
        # )
        print(request.json['token']['email'])
        customer = stripe.Customer.create(
            email=request.json['token']['email'],
            source=request.json['token']['id']
        )

        # stripe.Charge.create(
        #     customer=customer.id,
        #     amount=amount,
        #     currency='usd',
        #     description='Flask Charge'
        # )
        # float(request.json['product']['price'] * 100)

        print(type(int(request.json['product']['price'])))
        charge = stripe.Charge.create(
            amount=int(request.json['product']['price'] * 100),
            currency="usd",
            customer=customer.id,
            receipt_email=request.json['token']['email'],
            description='Purchased the : {}'.format(request.json['product']['name']),
            shipping={
                "name": request.json['token']['card']['name'],
                "address": {
                    "line1": request.json['token']['card']['address_line1'],
                    "line2": request.json['token']['card']['address_line2'],
                    "city": request.json['token']['card']['address_city'],
                    "country": request.json['token']['card']['address_country'],
                    "postal_code": request.json['token']['card']['address_zip']
                }
            })
        print("ssss")
        print(charge)
        return Response("success", status=200)

    except Exception as e:
        print("Exceptin")
        print(e)
        return Response(status=400)

    # return render_template('charge.html', amount=amount)


if __name__ == '__main__':
    app.run(debug=True)
