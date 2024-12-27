from ninja import Schema, FilterSchema
from typing import Optional
from pydantic import field_validator, Field

from django.db.models import Q

from datetime import datetime

class UserOut(Schema):
    id: int
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    

class RegisterSchema(Schema):
    username: str
    password: str
    confirm_password: str
    first_name: str
    last_name:  Optional[str]

    @field_validator('confirm_password')
    def validate_password(cls, confirm, form_data, **kwargs):
         print(confirm, form_data)
         if 'password' in form_data.data and confirm != form_data.data['password']:
            raise ValueError("Password dan konfirmasi tidak sama")
         return confirm
         
class CategoryIn(Schema):
    name: str

class CategoryOut(Schema):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

class TransactionIn(Schema):
    category_id: int
    amount: int
    description: str
    type: str
    transaction_date: str

class TransactionOut(Schema):
    id: int
    user: UserOut
    category: CategoryOut
    amount: int
    description: str
    type: str
    transaction_date: datetime
    created_at: datetime
    updated_at: datetime


class TransactionFilter(FilterSchema):
    search: Optional[str] = Field(default=None, q=['description__icontains'])
    type: Optional[str] = None
    transaction_date: Optional[str] = None
    
    def filter_type(self, value: str):
        return Q(type=self.type) if value else Q()
    
    def filter_date(self, value: str):
        return Q(transaction_date=datetime.strptime(self.transaction_date, '%Y-%m-%d').date()) if value else Q()
    
