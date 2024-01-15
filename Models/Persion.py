
from datetime import datetime
class Person:
    def __init__(self, first_name, last_name, phone_number, create_date=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        if create_date == None:
            t0 = datetime(1, 1, 1)
            now = datetime.utcnow()
            seconds = (now - t0).total_seconds()
            ticks = seconds * 10**7
            self.create_date=ticks
        else:
            self.create_date=create_date

    def __str__(self):
        Data={"First Name":self.first_name,"Last Name":self.last_name, "Phone":self.phone_number,"Craete Date":self.create_date}
        return Data

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update(self, first_name, last_name, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number