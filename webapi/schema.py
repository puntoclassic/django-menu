
from ninja import Schema
from ninja_jwt.schema import TokenObtainPairSerializer

class CategoryApiResponse(Schema):
    id: int
    name: str    
    image: str

class FoodApiResponse(Schema):
    id: int
    name: str    
    ingredients: str
    price: float

class UserSchema(Schema):
    first_name: str
    last_name: str
    verified: bool
    email: str

class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema

class MyTokenObtainPairSchema(TokenObtainPairSerializer):
    def output_schema(self):
        out_dict = self.dict(exclude={"password"})
        out_dict.update(user=UserSchema.from_orm(self._user))
        return MyTokenObtainPairOutSchema(**out_dict)