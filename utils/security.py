import datetime
import pytz
import jwt
import time
from decouple import config

class security():
    tz = pytz.timezone('America/Mexico_City')
    secret1 = config('SECRET_1')
    secret2 = config('SECRET_2')


    @classmethod
    def generate_token_user(cls, authenticated_user):
        now = datetime.datetime.now(tz=cls.tz)
        expiration = now + datetime.timedelta(hours=15)
        exp_unix = int(expiration.timestamp())  # Convertir a tiempo Unix

        payload = {
            'ia': now.isoformat(),
            'exp': exp_unix,  # Utilizar tiempo Unix en lugar de formato ISO
            'username': authenticated_user.id,
            'email': authenticated_user.email,
        }
        return jwt.encode(payload, cls.secret1, algorithm="HS256")
    
    @classmethod
    def verify_token_user(cls, headers):
        print('Authorization' in headers.keys())
        if 'Authorization' in headers.keys():
            autorization = headers['Authorization']
            encode_token = autorization.split(" ")[1]

            try:
                payload = jwt.decode(encode_token, cls.secret1, algorithms=["HS256"])
                return True
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                return False
        return False
    
    @classmethod
    def generate_token_restaurant(cls, authenticated_restaurant):
        now = datetime.datetime.now(tz=cls.tz)
        expiration = now + datetime.timedelta(hours=15)
        exp_unix = int(expiration.timestamp())  # Convertir a tiempo Unix

        payload = {
            'ia': now.isoformat(),
            'exp': exp_unix,  # Utilizar tiempo Unix en lugar de formato ISO
            'username': authenticated_restaurant.id,
            'email': authenticated_restaurant.email,
        }
        return jwt.encode(payload, cls.secret2, algorithm="HS256")
    
    @classmethod
    def verify_token_restaurant(cls, headers):
        print('Authorization' in headers.keys())
        if 'Authorization' in headers.keys():
            autorization = headers['Authorization']
            encode_token = autorization.split(" ")[1]

            try:
                print('aqui ando')
                payload = jwt.decode(encode_token, cls.secret2, algorithms=["HS256"])
                return True
            except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                return False
        return False