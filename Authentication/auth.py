from flask import Flask,jsonify
import sqlite3
from sanitization import details_validation
import logging
from datetime import datetime

logging.basicConfig(filename=r'C:\Users\HP\Desktop\Pk_space\Logs\access.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class security_verification():
    def __init__(self,dbname):
        # self.path=path
        self.conn=sqlite3.connect(dbname)
        self.cursor=self.conn.cursor()
        
    def user_details(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_log_details(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usernames TEXT NOT NULL,
                            password TEXT NOT NULL
                            )''')
        self.conn.commit()
        
    def user_signup(self, name, key):
        
        try:
            validator=details_validation(name,key)
        except ValueError as e:
            logging.warning(f"{datetime.now()} Validation Error | Request Path:{self.path}")
            return str(e)
        else:
            self.cursor.execute('SELECT * FROM user_log_details WHERE usernames=?',(name,))
            already_present=self.cursor.fetchone()
            if already_present:
                return "Username already present,Please enter another one"
            else:
                self.cursor.execute('INSERT INTO user_log_details(usernames, password) VALUES(?,?)',(name, key))
                self.conn.commit()
                return "Signed Up Successfully"
    
    def user_login_check(self,name,key):
        self.cursor.execute("SELECT * from user_log_details WHERE usernames=? and password=?",(name,key))   
        log=self.cursor.fetchone()
        if not log:
            return "User not found, Please Sign Up"
        else:
            return "logged in successfully"
        
        
        

