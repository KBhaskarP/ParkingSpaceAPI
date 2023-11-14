from twilio.rest import Client
from datetime import datetime
import logging
import configparser


logging.basicConfig(filename=r'C:\Users\HP\Desktop\Pk_space\Logs\access.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class bill_payment:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.sms_from=config.get('Credentials', 'DB_phone_number')
        self.sid=config.get('Credentials', 'DB_SID')
        self.token=config.get('Credentials', 'DB_TOKEN')
        
    def amount_calculator(self,total_hours):
        
        if total_hours >= 0 and total_hours <= 1:
            Amount_to_be_paid = 80
        elif total_hours > 1 and total_hours <= 2:
            Amount_to_be_paid = 110
        elif total_hours > 2 and total_hours <= 7:
            Amount_to_be_paid = 100 + (total_hours * 20)
        elif total_hours > 7 and total_hours < 24:
            Amount_to_be_paid = 300
        elif total_hours > 24:
            Amount_to_be_paid = 300 + (total_hours - 24) * 50
            
        return Amount_to_be_paid
    
    def send_message(self,driverName,numberPlate,entryTime,exitTime,entryDate,exitDate,companyName,phoneNumber):
        client=Client(self.sid, self.token)
        EntryTime=entryTime
        ExitTime=exitTime
        EntryDate=entryDate
        ExitDate=exitDate
        
        entry_datetime = datetime.strptime(EntryDate + " " + EntryTime, '%Y-%m-%d %H:%M')
        exit_datetime = datetime.strptime(ExitDate + " " + ExitTime, '%Y-%m-%d %H:%M')

        time_stayed = exit_datetime - entry_datetime

        total_hours = time_stayed.seconds // 3600
        total_minutes = (time_stayed.seconds % 3600) // 60

        amount=self.amount_calculator(total_hours)
        
        
        message = client.messages.create(
                from_=self.sms_from,
                body=f'''
                              RECIEPT
                    -------------------------
                    Driver: {driverName}
                    Vehicle: {numberPlate}
                    Entry Time: {entryTime} | Exit Time: {exitTime}
                    Entry Date: {entryDate} | Exit Date: {exitDate}
                    Company: {companyName}
                    Contact: {phoneNumber}
                    
                    
                    
                    
                    Total Time Stayed: {total_hours} hours and {total_minutes} minutes"
                    Total Amount: Rs.{amount}/- Only
                    UPI ID: xxxxxxx_UPI_ID_xxxxxxxx
                    
                    ''',
                to=phoneNumber
                )
        logging.info(f"{datetime.now()}---Bill Generated and Sent to {companyName}| id:{message.sid}")
        return "Done"
