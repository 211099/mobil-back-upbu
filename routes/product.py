from flask import Blueprint, request, jsonify, session, abort
from models.products import Products

from utils.db import db
from utils.security import security

from werkzeug.utils import secure_filename
from firebase_admin import storage 

products = Blueprint('products',__name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# CRUD

# nuevo prooducto
@products.route('/newProduct', methods=['POST'])

def add_product():
    has_acces = security.verify_token_restaurant(request.headers)
    print(has_acces)    
    if has_acces:
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        restaurant_id = request.form.get('restaurant_id')
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            blob = storage.bucket().blob(filename)
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
            blob.make_public()
            image_url = blob.public_url
        else:
            return "Invalid image", 400
        new_product = Products(name, description, price , image_url ,restaurant_id)
        db.session.add(new_product)
        db.session.commit()
        print(name, description, price)
        return 'agregar'
    else:
        response = jsonify({'message':'Unauthorized'})
        return response, 401

#actualizar el produxto
@products.route('/updateproduct/<int:id>', methods=['PUT'])
def update_product(id):
    has_acces = security.verify_token_restaurant(request.headers)
    if has_acces:
        product = Products.query.get(id)
        if not product:
            return jsonify({'message': 'Producto no encontrado'}), 404
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price

        db.session.commit()

        return jsonify({'message': 'Producto actualizado exitosamente'})
    else:
        response = jsonify({'message':'Unauthorized'})
        return response, 401

#eliminar el producto
@products.route('/delete/<id>', methods=['DELETE'])
def delete_product(id):
    has_acces = security.verify_token_restaurant(request.headers)
    if has_acces: 
        product = Products.query.get(id)
        if not product:
            return jsonify({'message': 'Producto no encontrado'}), 404
        db.session.delete(product)
        db.session.commit()
        print(product)
        return 'eliminar'
    else:
        response = jsonify({'message':'Unauthorized'})
        return response, 401



# obtener por list
@products.route("/restaurant/<restaurant_id>/products", methods=['GET'])
def get_restaurant_products(restaurant_id):
    has_acces = security.verify_token_restaurant(request.headers)
    if has_acces: 
        # Obtenemos todos los productos que coinciden con el restaurant_id especificado
        products = Products.query.filter_by(restaurant_id=restaurant_id).all()

        # Si no hay productos, retorna un mensaje de error
        if not products:
            return jsonify({'error': 'No products found for this restaurant'}), 404

        # Convertimos los productos a formato JSON
        products_list = []
        for product in products:
            products_list.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image_url': product.image_url,
                'restaurant_id': product.restaurant_id
            })

        return jsonify(products_list)
    else:
        response = jsonify({'message':'Unauthorized'})
        return response, 401

