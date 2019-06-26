from flask import request

from project.models import User
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
