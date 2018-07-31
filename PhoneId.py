from datetime import datetime, timedelta, time
class PhoneId:
    def __init__(self,phoneid,typeMessage,coordinate=[]):
        self.phoneid="phone_"+str(phoneid)
        self.coordinate=coordinate
        self.typeMessage=typeMessage

    def getMessage(self,file):
        if (file[0].find("@START") != 0):
            if (file[0].find("@END") != 0):
                timeArr = datetime.strptime(str(file[3]), '%H:%M:%S.%f')
                file[3] = (timeArr + timedelta(microseconds=1)).time()



class typeMessage:
    def __init__(self,coordinate,time):