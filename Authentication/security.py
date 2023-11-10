from flask import Flask
from Authentication.auth import security_verification
from Data_Cleaning.sanitization import details_validation


class verify_details():
    def __init__(self,request,dbase):
        self.request = request
        self.dbase = dbase
        
        
    def verify_login(self):
        name=self.request.headers.get('name')
        key=self.request.headers.get('key')
        validation=details_validation(name,key)
        if validation:
            check=security_verification(self.dbase)
            if check.user_login_check(name,key):
                return True
            else:
                return False
        
    def verify_signup(self):
        name=self.request.headers.get('name')
        key=self.request.headers.get('key')
        validation=details_validation(name,key)
        if validation:
            check=security_verification(self.dbase)
            if check.user_signup(name,key):
                return True
            else:
                return False
            
        
        
        
    