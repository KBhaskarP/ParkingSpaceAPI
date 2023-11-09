from twilio.rest import Client
from datetime import datetime

class bill_payment:
    def __init__(self):
        self.sms_from='+12312254891'
        self.sid="ACc70c64f97435dab79762b6f88e9062eb"
        self.token='735e70b7a7f7c66623ade0cfac98a42e'
    
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
        full_day=300

        if total_hours>=0 and total_hours<=1:
            Amount_to_be_paid=80
        elif total_hours>1 and total_hours<=2:
            Amount_to_be_paid=110
        elif total_hours>2 and total_hours<=7:
            Amount_to_be_paid=100+ (total_hours*20)
        elif total_hours>7 and total_hours<24:
            Amount_to_be_paid=300
        elif total_hours>24:
            Amount_to_be_paid=300+(total_hours-24)*50
            
        message = client.messages.create(
                from_=self.sms_from,
                body=f'''
                    Bill for Parking Services
                    -------------------------
                    Driver: {driverName}
                    Vehicle: {numberPlate}
                    Entry Time: {entryTime} | Exit Time: {exitTime}
                    Entry Date: {entryDate} | Exit Date: {exitDate}
                    Company: {companyName}
                    Contact: {phoneNumber}
                    |
                    |
                    |
                    |
                    Total Time Stayed: {total_hours} hours and {total_minutes} minutes"
                    Total Amount: {Amount_to_be_paid}
                    UPI ID: xxxxxxx
                    
                    ''',
                to=phoneNumber
                )
        return "Done"
