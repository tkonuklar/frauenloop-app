from project import ma
from project.models import User

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
