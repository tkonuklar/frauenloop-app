from flask import request, jsonify, abort
from project.models import User
from project.schemas import UserSchema
from project import app, db

@app.route('/')
def home_page():
    return 'This is a Bank Account App!!!'

# http://127.0.0.1:5000/balance?pin=1234&user_name=user2000
@app.route('/balance')
def display_balance():
    pin_number = request.args.get('pin') #
    user_name = request.args.get('user_name') #
    searchedUser = User.query.filter_by(name=user_name).first()
    if searchedUser:
        if pin_number == searchedUser.pin:  ## Check info is in DB ?
            return 'This is your current balance: {} EUR'.format(searchedUser.balance)
        else:
            return pin_error()
    else:
        return "user does not exist"


def pin_error():
    return 'Access denied: incorrect PIN.'

# http://127.0.0.1:5000/withdraw?pin=1234&user_name=user1&amount=50
@app.route('/withdraw')
def withdraw():
    pin_number = request.args.get('pin')
    user_name = request.args.get('user_name')
    amount = int(request.args.get('amount'))

    if amount > 2000:
        return 'You are not allowed to go over 2000 euro daily limit'
    else:
        user = User.query.filter_by(name=user_name).first()
        if user: 
            if pin_number == user.pin: 
                # current_balance = user.balance
                if amount <= user.balance:
                    #updated_balance = current_balance - amount
                    #user.balance = updated_balance
                    user.balance -= amount
                    db.session.commit()
                    return 'Withdrew {} EUR. New balance is: {} EUR.'.format(amount, balance)        
                else:
                    return 'You are not allowed to withdraw more money than you have on your account!'
            else:
                return pin_error()
        else: 
            return "User does not exist"
#http://127.0.0.1:5000/deposit?pin=1234&user_name=Nicole%20Brown&amount=2000
@app.route('/deposit')
def deposit():
    pin_number = request.args.get('pin')
    user_name = request.args.get('user_name')
    amount = int(request.args.get('amount'))

    if amount >= 3000:
        return 'You can not deposit money more than the 3000 Euro daily limit'
    else:
        user = User.query.filter_by(name=user_name).first()
        if user:
            if pin_number == user.pin:
                # user.balance = user.balance + amount
                user.balance += amount
                db.session.commit()
                return 'Deposited {} EUR. New balance is: {} EUR.'.format(amount,user.balance)        
            else:
                return pin_error()
        else:
            return 'User does not exist'

#http://127.0.0.1:5000/transfer?pin=1234&sender=Nicole%2Brown&receiver=Nicole&amount=50
@app.route('/transfer')
def transfer():
    pin_number = request.args.get('pin')
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')
    amount = int(request.args.get('amount'))

    if amount >= 3000:
        return 'You can not transfer money more than the 3000 Euro daily limit'
    else:
        sender = User.query.filter_by(name=sender).first()
        receiver = User.query.filter_by(name=receiver).first()
        if sender:
            if receiver:
                if pin_number == sender.pin:
                    if amount <= sender.balance:
                        sender.balance -= amount
                        receiver.balance += amount
                        db.session.commit()
                        return 'Transfer {} EUR. Sender balance is: {} EUR. Receiver balance is: {}'\
                    .format(amount,sender.balance,receiver.balance)        
                    else:
                        return 'You dont have enought amount of money in your acount!'
                else:
                    return pin_error()
            else:
                return 'Receiver does not exist' 
        else:
            return 'Sender does not exist'

@app.route('/users', methods=['GET'])
def get_users():
    user_schema = UserSchema(many=True)
    users = User.query.all()
    response = user_schema.dump(users).data
    return  jsonify(response)


@app.route('/users',methods=['POST'])
def create_user():
    data  = request.get_json()
    new_name = data['name']
    new_pin = int(data['pin'])
    new_balance = int(data['balance'])
    if not new_name and new_balance and new_pin:
        abort(400, description="Your fault client!!")
    else:
        # check user does exist
        user = User.query.filter_by(name=new_name).first()
        if user:
            abort(400,description="Upss! User already exists")
        else:
            new_user = User(name=new_name, pin=new_pin, balance=new_balance)
            db.session.add(new_user)
            db.session.commit()
            user_schema = UserSchema()
            response = user_schema.dump(new_user).data
            return jsonify(response)

#http://127.0.0.1:5000/users?name=Tugce&pin=1234 = can return a list of users whose name is Tugce
#http://127.0.0.1:5000/users/1 = return only user 1  = Tugce

# get resource  id 1
# GET /users/1
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id, "Baby, the perfect man does not exist, kisses !")
    user_schema = UserSchema()
    response = user_schema.dump(user).data
    return jsonify(response)

# update resource details
# PUT /users/1    Request Body : {'name'='John'}
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data  = request.get_json()
    new_name = data['name']
    new_pin = data['pin']
    new_balance = data['balance']
    user = User.query.get_or_404(user_id, "Baby, the perfect man does not exist, kisses !")
    user.name = new_name
    user.pin = new_pin
    user.balance = new_balance
    db.session.commit()
    user_schema = UserSchema()
    response = user_schema.dump(user).data
    return jsonify(response)

# delete resource which I selected
# DELETE /users/1
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id, "Baby, the perfect man does not exist, kisses !")
    db.session.delete(user)
    db.session.commit()
    return '', 204






