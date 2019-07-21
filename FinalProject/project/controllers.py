from flask import jsonify, request, abort
from jsonschema import validate  # to validate the request body
from project import app, db
from project.models import User, Account
from project.schemas import UserSchema, AccountSchema  # to serialize our Db Models

# Request body validation schemas
user_request_schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}, "pin": {"type": "number"}},
}
account_request_schema = {
    "type": "object",
    "properties": {"balance": {"type": "number"}, "ownerId": {"type": "number"}},
}


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "You call root url"})


### USER ###

# http://127.0.0.1:5000/users
# request body sample : {
# 	"name":"Sureyya",
# 	"pin": 1234
# }
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(
        force=True
    )  # force=True will make sure this works even if a client does not specify application/json
    validate(instance=data, schema=user_request_schema)
    user_name = data["name"]
    pin = data["pin"]
    user = User.query.filter_by(name=user_name).first()
    if user:
        abort(
            400, description="User is already exist"
        )  # for now we will abort, then work on exception handling
    else:
        user = User(name=user_name, pin=pin)
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        response = user_schema.dump(user).data
        return jsonify(response)
    return response


# http://127.0.0.1:5000/users
# no request body
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    response = user_schema.dump(users).data
    return jsonify(response)


# http://127.0.0.1:5000/users
# no request body
@app.route("/users/prety", methods=["GET"])
def get_users_prety():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    response = user_schema.dump(users).data
    return jsonify(response)


# http://127.0.0.1:5000/users/1
# no request body
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user_schema = UserSchema()
        response = user_schema.dump(user).data
        return jsonify(response)
    else:
        abort(404, description="User does not exist")


# http://127.0.0.1:5000/users
# request body sample : {
# 	"name":"Sureyya",
# 	"pin": 1111
# }
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json(
        force=True
    )  # force=True will make sure this works even if a client does not specify application/json
    validate(instance=data, schema=user_request_schema)
    user_name = data["name"]
    pin = data["pin"]
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.name = user_name
        user.pin = pin
        db.session.commit()
        user_schema = UserSchema()
        response = user_schema.dump(user).data
        return jsonify(response)
    else:
        abort(
            404, description="User does not exist"
        )  # for now we will abort, then work on exception handling


# http://127.0.0.1:5000/users/1
# no request body
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return "", 204
    else:
        abort(404, description="User not found")


### ACCOUNT ###

# http://127.0.0.1:5000/users/:user_id/accounts
# request body sample :
# {
# 	"balance": 1500
# }
@app.route("/users/<int:user_id>/accounts", methods=["POST"])
def create_account(user_id):
    data = request.get_json(
        force=True
    )  # force=True will make sure this works even if a client does not specify application/json
    validate(instance=data, schema=account_request_schema)
    balance = data["balance"]
    user = User.query.get_or_404(user_id, "User does not exist")
    account = Account(balance=balance, owner_id=user_id)
    db.session.add(account)
    db.session.commit()
    account_schema = AccountSchema()
    response = account_schema.dump(account).data
    return jsonify(response)


# http://127.0.0.1:5000/users/:user_id/accounts
@app.route("/users/<int:user_id>/accounts", methods=["GET"])
def get_user_accounts(user_id):
    user = User.query.get_or_404(user_id, "User does not exist")
    account_schema = AccountSchema(many=True)
    response = account_schema.dump(user.account).data
    return jsonify(response)


# http://127.0.0.1:5000/users/:user_id/accounts/:account_id
@app.route("/users/<int:user_id>/accounts/<int:account_id>", methods=["GET"])
def get_user_account_detail(user_id, account_id):
    user = User.query.get_or_404(user_id, "User does not exist")
    account = Account.query.get_or_404(account_id, "Account does not exist")
    account_schema = AccountSchema()
    response = account_schema.dump(account).data
    return jsonify(response)


# POST : http://127.0.0.1:5000/users/:user_id/accounts/:accountId/withdraw
# request body sample :
# {
# 	"amount": 30,
#   "pin": 1234
# }
@app.route("/users/<int:user_id>/accounts/<int:account_id>/withdraw", methods=["POST"])
def withdraw(user_id, account_id):
    data = request.get_json(force=True)
    amount = data["amount"]
    pin_number = data["pin"]
    if amount > 2000:
        abort(
            400, description="You are not allowed to go over 2000 euro daily limit"
        )
    else:
        user = User.query.get_or_404(user_id, "User does not exist")
        if pin_number == user.pin:
            account = Account.query.get_or_404(account_id, "Account does not exist")
            if amount <= account.balance:
                account.balance -= amount
                db.session.commit()
                account_schema = AccountSchema()
                response = account_schema.dump(account).data
                return jsonify(response)
            else:
                abort(
                    400,
                    description="You are not allowed to withdraw more money than you have on your account!",
                )
        else:
            abort(400, description="Pin is not correct")


# POST : http://127.0.0.1:5000/users/:user_id/accounts/:accountId/deposit
# request body sample :
# {
# 	"amount": 30,
#   "pin": 1234
# }
@app.route("/users/<int:user_id>/accounts/<int:account_id>/deposit", methods=["POST"])
def deposit(user_id, account_id):
    data = request.get_json(force=True)
    amount = data["amount"]
    pin_number = data["pin"]
    if amount > 2000:
        abort(400, description="You are not allowed to go over 2000 euro daily limit")
    else:
        user = User.query.get_or_404(user_id, "User does not exist")
        if pin_number == user.pin:
            account = Account.query.get_or_404(account_id, "Account does not exist")
            account.balance += amount
            db.session.commit()
            account_schema = AccountSchema()
            response = account_schema.dump(account).data
            return jsonify(response)
        else:
            abort(400, description="Pin is not correct")


# POST : http://127.0.0.1:5000/users/:user_id/accounts/:accountId/transfer
# request body sample :
# {
# 	"amount": 30,
#   "pin": 1234,
#   "receiverId": 2,
#   "receiverAccountId": 1
# }
@app.route("/users/<int:user_id>/accounts/<int:account_id>/transfer", methods=["POST"])
def transfer(user_id, account_id):
    data = request.get_json(force=True)
    amount = data["amount"]
    pin_number = data["pin"]
    receiver_id = data["receiverId"]
    receiver_account_id = data["receiverAccountId"]
    if amount > 2000:
        abort(400, description='You are not allowed to go over 2000 euro daily limit')
    else:
        sender = User.query.get_or_404(user_id, "Sender does not exist")
        if pin_number == sender.pin:
            sender_account = Account.query.get_or_404(account_id, "Sender Account does not exist")
            User.query.get_or_404(receiver_id, "Receiver user does not exist")
            receiver_account = Account.query.get_or_404(receiver_account_id, "Receiver Account does not exist")
            sender_account.balance -= amount
            receiver_account.balance += amount
            db.session.commit()
            account_schema = AccountSchema()
            response = account_schema.dump(receiver_account).data
            return jsonify(response)
        else:
            abort(400, description='Pin is not correct')
            

