from base64 import b64encode
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    text = 'Welcome to our shop!'
    return (f'<h1>{text}</h1>')


def binary_image(img):
    with open(img, 'rb') as f:
        binary = b64encode(f.read())
    return binary


img1 = binary_image('iphone11.png')
img2 = binary_image('iphone13.png')

products = [{'id': '0',
             'icon': str(img1),
             'name': 'iPhone 11',
             'description': 'Apple iPhone 11, 64 GB, black'},
            {'id': '1',
             'icon': str(img2),
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
    name = request.form.get('name')
    description = request.form.get('description')
    request.files['icon'].save('uploaded_icon.png')
    img = binary_image('uploaded_icon.png')
    product = {'id': id, 'icon': str(img), 'name': name, 'description': description}
    products.append(product)
    return jsonify({'Added product': product})


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.form
    if data.get('name') is not None:
        products[id]['name'] = data['name']
    if data.get('description') is not None:
        print(data['description'])
        products[id]['description'] = data['description']
    if request.files.get('icon') is not None:
        request.files['icon'].save('uploaded_icon.png')
        img = binary_image('uploaded_icon.png')
        products[id]['icon'] = str(img)
    return jsonify({'Updated product': products[id]})


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    products.remove(products[id])
    return 'Deletion done'


if __name__ == '__main__':
    app.run(debug=True)
