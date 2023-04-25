from db import base, db_string

def creating_tables():
    base.metadata.create_all(db_string)