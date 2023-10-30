import re


class form_validation():
    def __init__(self,car_data,name_data):
        self.car_num_validate(car_data)
        self.name_validate(name_data)
            
        
    def car_num_validate(self,car_data):
        word_pattern=r'^[A-Z]{2}\d{2}[A-Z]\d{4}$'
        num_pattern=r'^[A-Z]{2}\d{8}$'
        if not (re.match(word_pattern,car_data) or re.match(num_pattern,car_data)):
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
        if not isinstance(id, int):
            raise ValueError("ID must be an integer")
            
    