from flask import jsonify, request, abort
from jsonschema import validate # to validate the request body
from project import app, db
from project.models import User, Account
from project.schemas import UserSchema, AccountSchema # to serialize our Db Models

# Request body validation schemas
user_request_schema ={
     "type" : "object",
     "properties" : {
         "name" : {"type" : "string"},
         "pin" : {"type" : "number"},
     },
}
account_request_schema ={
     "type" : "object",
     "properties" : {
         "balance" : {"type" : "number"},
         "ownerId" : {"type" : "number"},
     },
}


@app.route('/', methods=['GET'])
def root():
    return  jsonify(
        {'message':'You call root url'}
        )

### USER ###

# http://127.0.0.1:5000/users
# request body sample : {
# 	"name":"Sureyya",
# 	"pin": 1234
# }
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(force=True) # force=True will make sure this works even if a client does not specify application/json
    validate(instance=data, schema=user_request_schema)
    user_name= data['name']
    pin = data['pin']
    user = User.query.filter_by(name=user_name).first()
    if user:
        abort(400, description='User is already exist') # for now we will abort, then work on exception handling
    else:
        user = User(name = user_name, pin = pin)
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()  
        response = user_schema.dump(user).data
        return jsonify(response)
    return response

# http://127.0.0.1:5000/users
# no request body
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)  
    response = user_schema.dump(users).data
    return jsonify(response)

# http://127.0.0.1:5000/users
# no request body
@app.route('/users/prety', methods=['GET','PUT'])
def get_users_prety():
    users = User.query.all()
    user_schema = UserSchema(many=True)  
    response = user_schema.dump(users).data
    return jsonify(response)

# http://127.0.0.1:5000/users/1 
# no request body
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user_schema = UserSchema()  
        response = user_schema.dump(user).data
        return jsonify(response)
    else:
        abort(404, 'User does not exist')

# http://127.0.0.1:5000/users
# request body sample : {
# 	"name":"Sureyya",
# 	"pin": 1111
# }
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(force=True) # force=True will make sure this works even if a client does not specify application/json 
    validate(instance=data, schema=user_request_schema)
    user_name= data['name']
    pin = data['pin']
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.name = user_name
        user.pin = pin
        db.session.commit()
        user_schema = UserSchema()  
        response = user_schema.dump(user).data
        return jsonify(response)
    else:
        abort(404, description='User does not exist') # for now we will abort, then work on exception handling

# http://127.0.0.1:5000/users/1
# no request body
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return '', 204
    else:
        abort(404, 'User not found')


### ACCOUNT ###

# http://127.0.0.1:5000/accounts
# request body sample : 
# {
# 	"balance": 1500,
# 	"ownerId": 1
# }
@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json(force=True) # force=True will make sure this works even if a client does not specify application/json
    validate(instance=data, schema=account_request_schema)
    balance = data['balance']
    owner_id = data['owner']
    user = User.query.filter_by(id=owner_id).first()
    if user:
        account = Account(balance = balance, owner_id = owner_id)
        db.session.add(account)
        db.session.commit()
        account_schema = AccountSchema()  
        response = account_schema.dump(account).data
        return jsonify(response)
    else:
         abort(404, description='Owner does not exist') # for now we will abort, then work on exception handling

