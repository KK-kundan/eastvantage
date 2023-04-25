from sqlalchemy import Column, String, Float
from db import base
import uuid

class AddressBook(base):
    __tablename__='address_book'
    
    id=Column(String, default=uuid.uuid4())
    latitude=Column(Float, primary_key=True)
    longitude=Column(Float, primary_key=True)
    location_name=Column(String)

    