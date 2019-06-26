from project import ma
from project.models import User, Account

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class AccountSchema(ma.ModelSchema):
    class Meta:
        model = Account