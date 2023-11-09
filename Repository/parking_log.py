import sqlite3
from flask import jsonify,send_file
import pandas as pd
from Repository.company_log import company_details

class parking_space:
    def __init__(self,db_name):
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS parking_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver TEXT,
            car_number TEXT,
            entry_time TEXT,
            entry_date TEXT,
            exit_time TEXT,
            exit_date TEXT,
            company_num INTEGER,
            status TEXT
            
            
            )''')
        self.conn.commit()
    def customer_details(self,rec_id):
        self.cursor.execute('SELECT driver,car_number,entry_time,exit_time,entry_date, exit_date,company_num FROM parking_log WHERE id=?',(rec_id,))
        result=self.cursor.fetchone()
        if result:
            Driver_name,Number_plate,Time_of_entry,Time_of_exit,Date_of_entry,Date_of_exit,Company_Token=result
            return Driver_name,Number_plate,Time_of_entry,Time_of_exit,Date_of_entry,Date_of_exit,Company_Token
        else:
            return "No Relevant Information Found"
        
    def get_table(self):
        self.cursor.execute('SELECT * FROM parking_log')
        result=self.cursor.fetchall()
        if not result:
            return "No Records Available!"
        else:
            return jsonify(result)
        
        
    def get_records(self,sts):
        if sts not in ('Done','In_progress'):
            return 'Invalid Status Code, Use "Done" or "In_progress" only'
        
        self.cursor.execute('SELECT * FROM parking_log WHERE status=?',(sts,))
        result=self.cursor.fetchall()
        if not result:
            return "No Such Records Available!"
        else:
            query=(f'SELECT * FROM parking_log WHERE status="{sts}"')
            df=pd.read_sql_query(query,self.conn)
            df.to_csv(r'C:\Users\HP\Desktop\Pk_space\Logs\Records.csv',index=False) 
            self.conn.close()
            return send_file('Logs\Records.csv',as_attachment=True)
            # return jsonify(result)
            
            
        
    def insert_records(self,Driver,Car_num,Entry_time,Entry_date,Exit_time,Exit_date,Number,Status):
        self.cursor.execute('SELECT * FROM parking_log WHERE car_number=? AND status=?',(Car_num,"In_progress"))
        output=self.cursor.fetchall()
        if not output:
            self.cursor.execute('INSERT INTO parking_log (driver,car_number,entry_time,entry_date,exit_time,exit_date,company_num,status) VALUES (?,?,?,?,?,?,?,?)',(Driver,Car_num,Entry_time,Entry_date,Exit_time,Exit_date,Number,Status))
            self.conn.commit()
            return "Added Successfully"
        else:
            return "Record already present, Kindly contact the Authority."

    
    
    def update_records(self,Record_id,Exit_time,Exit_date):
        self.cursor.execute('''UPDATE parking_log
                            SET exit_time=?, exit_date=?, status=?
                            WHERE id=?''',(Exit_time,Exit_date,"Done",Record_id))
        self.conn.commit()
        return "Record Update Successfully"
    
    
    
    def delete_records(self,Record_id):
        self.cursor.execute('SELECT status from parking_log WHERE id=?',(Record_id,))
        record=self.cursor.fetchone()
        
        if record and record[0]=="Done":
            return "Record Already Logged In, Cannot Delete It"
        else:
            self.cursor.execute('DELETE FROM parking_log WHERE id=? and status=?',(Record_id,'In_progress'))
            self.conn.commit()
            return "Record Deleted Successfully"
        
    
    def delete_multiple_records(self,*Record_id):
        Deleted_id=[]
        Non_deleted_id=[]
        for id in Record_id:
            self.cursor.execute('SELECT status from parking_log WHERE id=?',(id,))
            record=self.cursor.fetchone()
            
            if record and record[0]=="Done":
                Non_deleted_id.append(id)
                # return "Record Already Logged In, Cannot Delete It"
            else:
                self.cursor.execute('DELETE FROM parking_log WHERE id=? and status=?',(id,'In_progress'))
                self.conn.commit()
                Deleted_id.append(id)
                # return "Record Deleted Successfully"
            
        if not Deleted_id:
            return f"All provided records ({', '.join(map(str, Non_deleted_id))}) were already logged in and cannot be deleted."
        elif not Non_deleted_id:
            return f"All provided records ({', '.join(map(str, Deleted_id))}) were successfully deleted."
        else:
            return f"Records deleted successfully. Deleted IDs: {', '.join(map(str, Deleted_id))}, Non-deleted IDs: {', '.join(map(str, Non_deleted_id))}."
             
    def close_connection(self):
        self.conn.close()    

        
        
        