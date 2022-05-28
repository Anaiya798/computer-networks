from flask import *

from shop_products import products
from tokenization import generate_token, tokens
from user_database import users

app = Flask(__name__)


@app.route('/')
def index():
    return (f'<h1>Welcome to our shop!</h1>')


@app.route('/products/', defaults={'token': None}, methods=['GET'])
@app.route('/products/<token>', methods=['GET'])
def get_all_products(token):
    ans = []
    if token is None:
        for product in products:
            if product['category'] == 'base':
                ans.append(product)
        return jsonify({'Products': ans})
    elif token not in tokens:
        return (f'<h3>Invalid token: {token} </h3>')
    return jsonify({'Products': products})


@app.route('/products/<int:id>', defaults={'token': None}, methods=['GET'])
@app.route('/products/<int:id>/<token>', methods=['GET'])
def get_product(id, token):
    if (token is not None) and (token not in tokens):
        return (f'<h3>Invalid token: {token} </h3>')
    return jsonify({'Selected product': products[id]})


@app.route('/products', defaults={'token': None}, methods=['POST'])
@app.route('/products/<token>', methods=['POST'])
def add_product(token):
    if (token is not None) and (token not in tokens):
        return (f'<h3>Invalid token: {token} </h3>')

    id = str(int(products[len(products) - 1]['id']) + 1)
    data = request.get_json(force=True)
    product = {'id': id, 'name': data['name'], 'category': data['category'], 'description': data['description']}

    if data['category'] == 'base' or data['category'] == 'pro':
        products.append(product)
    else:
        return (f'<h3>Invalid category: {data["category"]} </h3>')

    return jsonify({'Added product': product})


@app.route('/products/<int:id>', defaults={'token': None}, methods=['PUT'])
@app.route('/products/<int:id>/<token>', methods=['PUT'])
def update_product(id, token):
    if (token is not None) and (token not in tokens):
        return (f'<h3>Invalid token: {token} </h3>')

    data = request.get_json(force=True)
    if data.get('name') is not None:
        products[id]['name'] = data['name']
    if data.get('description') is not None:
        products[id]['description'] = data['description']
    if data.get('category') is not None:
        if data['category'] == 'base' or data['category'] == 'pro':
            products[id]['category'] = data['category']
        else:
            return (f'<h3>Invalid category: {data["category"]} </h3>')

    return jsonify({'Updated product': products[id]})


@app.route('/products/<int:id>', defaults={'token': None}, methods=['DELETE'])
@app.route('/products/<int:id>/<token>', methods=['DELETE'])
def delete_product(id, token):
    if (token is not None) and (token not in tokens):
        return (f'<h3>Invalid token: {token} </h3>')
    products.remove(products[id])
    return 'Deletion done'


@app.route('/login', defaults={'token': None}, methods=['GET', 'POST'])
@app.route('/login/<token>', methods=['GET', 'POST'])
def login_page(token):
    if (token is not None) and (token not in tokens):
        return (f'<h3>Invalid token: {token} </h3>')
    login = request.form.get('e-mail')
    password = request.form.get('password')
    if request.method == 'POST':
        if login not in users.keys() or password not in users.values():
            flash('User does not exist!')
        else:
            token = generate_token()
            flash(f'Successful! Your personal access token: {token}')

    return render_template('login.html')


@app.route('/register', defaults={'token': None}, methods=['GET', 'POST'])
@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    if (token is not None) and (token not in tokens):
        return (f'<h3>Invalid token: {token} </h3>')
    login = request.form.get('e-mail')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        elif login in users.keys():
            flash('E-mail alredy exists!')
        else:
            flash('Successful!')
            users[login] = password
        print(users)
    return render_template('register.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)
