
from typing import Optional

from fastapi import Form
from pydantic import BaseModel
from beanie import Document


#class Todo() 괄호안에 상속받고자하는걸 쓰면 상속이됨
# class Todo(BaseModel):
#     id: Optional[int] = None
#     item: str

class Todo(Document):
    # id: Optional[int] = None
    item: str

    @classmethod
    def as_form(cls, item: str =Form()):
        return cls(item=item)

    class Setting:
        name = 'todo'

    class Config:
        json_schema_extra = {
            "example" : {
                "id" : 1,
                "item" : "Example Schema!"
            }
        }



class TodoItem(BaseModel):
    item: str

    class Config:
        json_schema_extra = {
            "example": {
                "item": "Read the next chapter of the book"
            }
        }