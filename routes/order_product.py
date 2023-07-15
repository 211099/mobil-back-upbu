from flask import Blueprint, request, jsonify, make_response, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.order_products import Orders_products

from utils.forms_user import RegiterForm
from utils.forms_user import LoginForm

from utils.db import db

orders_products = Blueprint('orders_products',__name__)