import re

class details_validation():
    def __init__(self,name,key):
        self.username_check(name)
        self.key_check(key)
        
    def username_check(self,name):
        username_pattern=r'^[a-zA-Z0-9_]{3,20}$'
        if not (re.match(username_pattern,name)):
            raise ValueError("Enter a valid username")
        else:
            return True
        
    def key_check(self,key):
        password_pattern=r'[a-zA-Z0-9_\.]{8,16}$'
        if not (re.match(password_pattern,key)):
            raise ValueError("Enter a valid password not more than 16 charecters including (Aa-Zz|0-9|_\.)")
        else:
            return True
class form_validation():
    def __init__(self,car_data,name_data):
        self.car_num_validate(car_data)
        self.name_validate(name_data)
            
        
    def car_num_validate(self,car_data):
        word_pattern=r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$'
    
        if not (re.match(word_pattern,car_data)):
            raise ValueError("Invalid Car Number")
    
    def name_validate(self,name_data):
        if not name_data :
            raise ValueError("One Or More Null Entry")
        if not re.match(r'^[a-zA-Z\s]+$',name_data):
            raise ValueError("Name in Unrecognized Format")
        
        
class id_validation():
    def __init__(self,rec_id):
        self.id_validate(rec_id)
        
    def id_validate(self,rec_id):
        if not rec_id:
            raise ValueError("One Or More Null Entry")
        if not rec_id.isdigit():
            raise ValueError("ID must be an integer")
            
    