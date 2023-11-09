from flask import jsonify
import sqlite3

class company_details:
    def __init__(self,db_name):
        self.conn=sqlite3.connect(db_name)
        self.cursor=self.conn.cursor()
        
    def create_company_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS company_log(
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            company_loc TEXT NOT NULL,
            contact TEXT NOT NULL
            )''')
        self.conn.commit()
        
    def get_company_table(self):
        self.cursor.execute('SELECT * FROM company_log')
        result=self.cursor.fetchall()
        if not result:
            return "No Records Available!"
        else:
            return jsonify(result)
        
    def insert_company_records(self,c_name,c_loc,c_contact):
        self.cursor.execute('SELECT * FROM company_log WHERE company_name=?',(c_name,))
        output=self.cursor.fetchall()
        if not output:
            self.cursor.execute('INSERT INTO company_log (company_name,company_loc,contact) VALUES (?,?,?)',(c_name,c_loc,c_contact))
            self.conn.commit()
            return "Added Successfully"
        else:
            return "Record already present, Kindly contact the Authority."
        
    def update_company_records(self,c_id,c_name,c_loc,c_contact):
        self.cursor.execute('''UPDATE parking_log
                            SET company_name=?, company_loc=?, contact=?
                            WHERE id=?''',(c_name,c_loc,c_contact,c_id))
        self.conn.commit()
        return "Record Updated Successfully"
    
    def delete_company_records(self,c_id):
        
        self.cursor.execute('DELETE FROM parking_log WHERE id=? and status=?',(c_id,))
        self.conn.commit()
        return "Record Deleted Successfully"
    
    def company_info(self,org_id):
        self.cursor.execute('SELECT company_name,contact FROM company_log WHERE company_id=?',(org_id,))
        result=self.cursor.fetchone()
        if result:
            company,phone=result
            return company,phone
        else:
            return "No Relevant Records Found"
        
    def close_connection(self):
        self.conn.close() 