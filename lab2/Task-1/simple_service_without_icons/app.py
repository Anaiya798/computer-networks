from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    text = 'Welcome to our shop!'
    return (f'<h1>{text}</h1>')


products = [{'id': '0',
             'name': 'iPhone 11',
             'description': 'Apple iPhone 11, 64 GB, black'},
            {'id': '1',
             'name': 'iPhone 13',
             'description': 'Apple iPhone 13, 256GB, black'}
            ]


@app.route('/products', methods=['GET'])
def get_all_products():
    return jsonify({'Products': products})


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    return jsonify({'Selected product': products[id]})


@app.route('/products', methods=['POST'])
def add_product():
    id = str(int(products[len(products) - 1]['id']) + 1)
    data = request.get_json(force=True)
    product = {'id': id, 'name': data['name'], 'description': data['description']}
    products.append(product)
    return jsonify({'Added product': product})


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json(force=True)
    if data.get('name') is not None:
        products[id]['name'] = data['name']
    if data.get('description') is not None:
        products[id]['description'] = data['description']
    return jsonify({'Updated product': products[id]})


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    products.remove(products[id])
    return 'Deletion done'


if __name__ == '__main__':
    app.run(debug=True)
