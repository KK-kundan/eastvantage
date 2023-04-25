from pydantic import BaseModel

class AddressData(BaseModel):
    latitude:float
    longitude:float
    location_name:str