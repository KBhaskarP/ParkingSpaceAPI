from flask import request
from datetime import datetime
from Repository.parking_log import parking_space
from Repository.company_log import company_details
from sanitization import form_validation,id_validation
import logging
from payment.send_bill import bill_payment



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
    
    def get_company(self):
        output=self.dbase.get_company_table()
        self.dbase.close_connection()
        logging.info(f"{datetime.now()}---Company Table Accessed | Request Path:{self.path}")
        return output
        
    def post_action(self):
        current_datetime=datetime.now()
        name=self.request.form['driver']
        car_number=self.request.form['CarNumber']
        number=self.request.form['Number']
        
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
            output=self.dbase.insert_records(name,car_number,entry_time,entry_date,exit_time,exit_date,number,status)
            logging.info(f"{current_datetime}---Table Updated With New Record | Request Path:{request.path}")
            self.dbase.close_connection()
            return output
        
    def post_company(self):
        name=self.request.form['company_name']
        loc=self.request.form['company_location']
        contacts=self.request.form['company_contact']
        output=self.dbase.insert_company_records(name,loc,contacts)
        logging.info(f"{datetime.now()}---Company Table Updated With New Record | Request Path:{request.path}")
        self.dbase.close_connection()
        return "Company Added Successfully"
        
            
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
            
            customer=parking_space('logs.db')
            driver, number_plate, entry_time, Exit_time, entry_date, Exit_date, company_token=customer.customer_details(rec_id)
            customer.close_connection()
            
            com=company_details('logs.db')
            company_name, phone_number=com.company_info(company_token)
            com.close_connection()
            
            self.dbase.close_connection()
            bill=bill_payment()
            result=bill.send_message(driver, number_plate, entry_time, Exit_time, entry_date, Exit_date,company_name, phone_number)
            
            if result=="Done":
                return f"Bill Sent to {company_name} for {driver} on {exit_time}|{exit_date}"
            else:
                "SomeError Occured"
            
            
        
        
    def update_company(self):
        id=self.request.form['company_id']
        name=self.request.form['company_name']
        loc=self.request.form['company_location']
        contacts=self.request.form['company_contact']
        output=self.dbase.update_company_records(id,name,loc,contacts)
        logging.info(f"{datetime.now()}---Record with ID: {id} Modified | Request Path:{self.path}")
        self.dbase.close_connection()
        return "Company Table updated successfully"
        
    
        
        
        
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
    
    def delete_company(self):
        id=self.request.form['c_id']
        output=self.dbase.delete_company_records(id)
        logging.info(f"{datetime.now()}---Record with ID: {id} Deleted | Request Path:{self.request.path}")
        self.dbase.close_connection()
        return "Record From Company deleted"
        
        
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