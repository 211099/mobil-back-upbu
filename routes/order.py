from flask import Blueprint, request, jsonify, make_response, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.orders import Orders
from utils.forms_user import RegiterForm
from utils.forms_user import LoginForm

from utils.db import db

orders = Blueprint('orders',__name__)


