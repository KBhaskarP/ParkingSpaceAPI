from flask import Flask,request
from datetime import datetime
from Repository.parking_log import parking_space
from sanitization import form_validation,id_validation
import logging

logging.basicConfig(filename=r'C:\Users\HP\Desktop\Pk_space\Logs\access.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ActionHandling():
    def __init__(self,request,dbase,path):
        self.request = request
        self.dbase=dbase
        self.path=path
        
    def get_action(self):
        output=self.dbase.get_table()
        self.dbase.close_connection()
        logging.info(f"{datetime.now()}---Table Accessed | Request Path:{self.path}")
        return output
        
    def post_action(self):
        current_datetime=datetime.now()
        name=self.request.form['driver']
        car_number=self.request.form['CarNumber']
        
        try:
            validator=form_validation(car_number,name)
        except ValueError as e:
            logging.critical(f"{current_datetime} Validation Error | Request Path:{self.path}")
            return str(e)
        else:
            entry_time=str(current_datetime.time())[:5]
            entry_date=str(current_datetime.date())
            exit_time=None
            exit_date=None
            status="In_progress"
            output=self.dbase.insert_records(name,car_number,entry_time,entry_date,exit_time,exit_date,status)
            logging.info(f"{current_datetime}---Table Updated With New Record | Request Path:{request.path}")
            self.dbase.close_connection()
            return output
            
    def update_action(self):
        current_datetime=datetime.now()
        rec_id=self.request.form['id']
        try:
            validator=id_validation(rec_id)
        except ValueError as e:
            logging.critical(f"{current_datetime} Validation Error | Request Path:{self.path}")
            return str(e)
        else:
            
            exit_time=str(current_datetime.time())[:5]
            exit_date=str(current_datetime.date())
            output=self.dbase.update_records(rec_id,exit_time,exit_date)
            logging.info(f"{current_datetime}---Record with ID: {rec_id} Modified | Request Path:{self.path}")
            self.dbase.close_connection
            return output
    def delete_single_record(self):
        rec_id=self.request.form['id']
        try:
            validator=id_validation(rec_id)
        except ValueError as e:
            logging.critical(f"{datetime.now()} Validation Error | Request Path:{self.request.path}")
            return str(e)
        else:
            output=self.dbase.delete_records(rec_id)
            if "Sucessfully deleted" in output:
                logging.info(f"{datetime.now()}---Record with ID: {rec_id} Deleted | Request Path:{self.request.path}")
                self.dbase.close_connection()
                return output
            else:
                logging.critical(f"{datetime.now()}--- Logged in record with ID: {rec_id} attempted to delete | Request Path:{self.request.path}")
        return output
    
    def delete_multiple_records(self):
        rec_id=self.request.json.get("id")
        output=self.dbase.delete_multiple_records(*rec_id)
        if "cannot be deleted" in output:
            
            logging.critical(f"{datetime.now()} Logged in Records attempted to Delete | Request Path:{self.request.path}")
            self.dbase.close_connection()
            
        else:
            
            logging.info(f"{datetime.now()}---Multiple Records Deleted | Request Path:{self.request.path}")
            self.dbase.close_connection()
            return output
        
    def downloadcsv(self):
        stat=self.request.form['status']
        self.dbase.get_records(stat)
        logging.critical(f"{datetime.now()} Records with Status:{stat} downloaded | Request Path:{self.request.path}")
        return "Downloaded Successfully"