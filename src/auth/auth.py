#########################################################
#I# IMPORTS
#########################################################
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

#########################################################
#I# AUTH0 Settings
#########################################################
AUTH0_DOMAIN = 'fsnd-capstone2-tenant.eu.auth0.com'  
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fsnd-capstone2-api-identifier'   

#########################################################
#I# AuthError Exception
#########################################################
'''
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

#########################################################
#I# GET THE TOKEN FROM THE AUTH HEADER
#########################################################
'''
- Attempt to get the header from the request
- Raise an AuthError if no header is present
- Attempt to split bearer and the token
- Raise an AuthError if the header is malformed
- Return the token part of the header
'''
def get_token_auth_header():
   
    auth = request.headers.get('Authorization', None)
    if not auth:
       raise AuthError({
           'code': 'authorization_header_missing',
           'description': 'Authorization header is expected.'
       }, 401)
   
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)
    
    token = parts[1]
    return token

#########################################################
#I# check_permissions(permission, payload) method
#########################################################
'''
    - INPUTS:
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    - Raise an AuthError if permissions are not included in the payload
    - Raise an AuthError if the requested permission string is not in the payload permissions array
    - Return true otherwise
'''
def check_permissions(permission, payload):

    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)

    return True


#########################################################
#I# verify_decode_jwt(token) method
#########################################################
'''
    - INPUTS:
        token: a json web token (string)

    - Verify: 
        - Auth0 token with key id (kid)
        - the token using Auth0 /.well-known/jwks.json
    - Decode the payload from the token
    - Validate the claims
    - Return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    # get the public key from Auth0
    jsonurl = urlopen(f'https://fsnd-capstone-tenant.eu.auth0.com/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # get the data from the token header
    unverified_header = jwt.get_unverified_header(token)

    # choose the key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            # use the key to validate the jwt
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


#########################################################
#I# @requires_auth(permission) decorator method
#########################################################
'''
    - INPUTS:
        permission: string permission (i.e. 'post:drink')

    - Get the token using the get_token_auth_header method
    - Decode the jwt using the verify_decode_jwt method 
    - Validate claims and check the requested permission using the check_permissions method
    - Return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):    
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator



