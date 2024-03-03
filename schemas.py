from pydantic import BaseModel
from typing import Optional

class SignupModel(BaseModel):
    # id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'username': 'admin',
                'email': 'admin@aa.aa',
                'password': 'pass',
                'is_staff': False,
                'is_active': True,
            }
        }
