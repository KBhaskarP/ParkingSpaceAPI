from flask import Flask,request
from Repository.parking_log import parking_space
import logging
from api_action import ActionHandling
from Authentication.security import verify_details
from Authentication.auth import security_verification


app=Flask(__name__)

dbase=parking_space('logs.db')
dbase.create_table()

security_dbase=security_verification('Isecurity.db')
security_dbase.user_details()


@app.route('/signup', methods=['POST'])
def signup():
    
    establish_entry=verify_details(request,'Isecurity.db',request.path)
    result=establish_entry.verify_signup()
    if result:
        return "Voila! Signed Up Successfully"
    else:
        return "Username Already in use"
    

@app.route('/parkinglog',methods=['GET'])
def get_parkinglog():
    verify_entry=verify_details(request,'Isecurity.db')
    result=verify_entry.verify_login()
    if result:   
        dbase=parking_space('logs.db')
        fetch_data=ActionHandling(request,dbase,request.path)
        return fetch_data.get_action()
    else:
        message = "Inavlid username or password"
        return message
    
    
    
    
@app.route('/EntryParkinglog',methods=['POST'])
def enter_parkinglog():
    verify_entry=verify_details(request,'Isecurity.db')
    result=verify_entry.verify_login()
    if result:
        dbase=parking_space('logs.db')
        post_data=ActionHandling(request,dbase,request.path)
        return post_data.post_action()
    else:
        message = "Inavlid username or password"
        return message
    
        
       
@app.route('/UpdateParkinglog',methods=['PUT'])
def update_parkinglog(): 
    verify_entry=verify_details(request,'Isecurity.db')
    result=verify_entry.verify_login()
    if result:
        dbase=parking_space('logs.db')
        update_data=ActionHandling(request,dbase,request.path)
        return update_data.update_action()
    else:
        message = "Inavlid username or password"
        return message
        
@app.route('/DeleteParkinglog',methods=['DELETE'])
def delete_parkinglog():  
    verify_entry=verify_details(request,'Isecurity.db')
    result=verify_entry.verify_login()
    if result:
        dbase=parking_space('logs.db')
        delete_data=ActionHandling(request,dbase,request.path)
        return delete_data.delete_single_record()
    else:
        message = "Inavlid username or password"
        return message

@app.route('/multidelete',methods=['DELETE'])
def multi_delete():
    verify_entry=verify_details(request,'Isecurity.db')
    result=verify_entry.verify_login()
    if result:
        dbase=parking_space('logs.db')
        multi_delete=ActionHandling(request,dbase,request.path)
        return multi_delete.delete_multiple_records()
    else:
        message = "Inavlid username or password"
        return message
    
@app.route('/download',methods=['POST'])
def download_data():
    verify_entry=verify_details(request,'Isecurity.db')
    result=verify_entry.verify_login()
    if result:
        dbase=parking_space('logs.db')
        download_data=ActionHandling(request,dbase,request.path)
        return download_data.downloadcsv()
    else:
        message = "Inavlid username or password"
        return message

if __name__ == '__main__':
    app.run(debug=True)