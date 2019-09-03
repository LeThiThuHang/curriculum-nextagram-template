from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.image import Image

import os

class Payment(BaseModel):
    image = pw.ForeignKeyField(Image, backref='payments', null=False) # the backref is the same name as the DB column name
    user = pw.ForeignKeyField(User, backref='payments', null=False)
    amount = pw.DecimalField(null=False)

    def validate(self):
        return self.errors