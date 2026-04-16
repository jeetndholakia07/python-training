import uuid

def generateGUID():
    return str(uuid.uuid4())

def is_valid_guid(guid:str):
    try:
        uuid.UUID(str(guid),version=4)
        return True
    except ValueError:
        return False