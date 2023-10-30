from flask import Flask,request,send_file
from parking_log import parking_space
from datetime import datetime
from sanitization import form_validation,id_validation
import pandas as pd

app=Flask(__name__)

# text/html; charset=utf-8
dbase=parking_space('logs.db')
dbase.create_table()

@app.route('/parkinglog',methods=['GET', 'POST','PUT','DELETE'])
def get_parkinglog():
    dbase=parking_space('logs.db')
    current_datetime=datetime.now()
    
    if request.method == 'GET':
        output=dbase.get_table()
        dbase.close_connection()
        return output
        
    if request.method=="POST":
        name=request.form['driver']
        car_number=request.form['CarNumber']
        
        try:
            validator=form_validation(car_number,name)
        except ValueError as e:
            return str(e)
        else:
            
            entry_time=str(current_datetime.time())[:5]
            entry_date=str(current_datetime.date())
            exit_time=None
            exit_date=None
            status="In_progress"
            output=dbase.insert_records(name,car_number,entry_time,entry_date,exit_time,exit_date,status)
            dbase.close_connection()
            return output
        
    
    if request.method == 'PUT':
        rec_id=request.form['id']
        try:
            validator=id_validation(rec_id)
        except ValueError as e:
            return str(e)
        else:
            exit_time=str(current_datetime.time())[:5]
            exit_date=str(current_datetime.date())
            output=dbase.update_records(rec_id,exit_time,exit_date)
            dbase.close_connection
            return output
        
    return "Invalid Response"
    
@app.route('/multidelete',methods=['DELETE'])
def multi_delete():
    dbase=parking_space('logs.db')
    if request.method=="DELETE":
        rec_id=request.json.get("id")
        output=dbase.delete_multiple_records(*rec_id)
        dbase.close_connection()
        return output
    return "Invalid Response"
    
@app.route('/download',methods=['POST'])
def download_data():
    dbase=parking_space('logs.db')
    if request.method == 'POST':
        stat=request.form['status']
        dbase.get_records(stat)
        return "Downloaded Successfully"
          
    return "Invalid Request"
    



if __name__ == '__main__':
    app.run(debug=True)