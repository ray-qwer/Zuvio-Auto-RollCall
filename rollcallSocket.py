import requests
from bs4 import BeautifulSoup as bs 
import re
import time
import tkinter as tk
import pickle
# global variables

loginURL = "https://irs.zuvio.com.tw/irs/submitLogin"
rollcallURL = 'https://irs.zuvio.com.tw/app_v2/makeRollcall/'
userInfo = {                        
        "email": "",\
        "password": "",\
        "url":"",\
        "lat":25.016168,\
        "lng":121.545303,
        "timePeriod":60
}
# 25.016168, 121.545303 男三舍位置
class zuvio:
    def __init__(self,mail,password,courseURL,lat,lng,timePeriod):
        self.rs = requests.Session()
        self.userMail = mail
        self.password = password
        self.userID = 0
        self.accessToken = ""
        self.rollcall_id = ""
        self.courseURL = courseURL  # the URL of the lesson you need to rollcall
        self.lat = lat
        self.lng = lng
        self.timePeriod = timePeriod
        self.warningMessage = ""
    def login(self):
        formData = {
            "email": self.userMail,
            "password": self.password,
            "current_language": "zh-TW"
        }
        loginReq = self.rs.post(url = loginURL, data=formData)
        if loginReq.status_code != 200:
            self.warningMessage = ("please check your internet connection!!")
            return False
        regex_userID = re.compile(r"var user_id = (\w{0,})")
        regex_accessToken = re.compile(r"var accessToken = \"(\w{0,})")
        try: 
            self.userID = int(regex_userID.search(loginReq.text).group(1))
            self.accessToken = regex_accessToken.search(loginReq.text).group(1)
        except:
            self.warningMessage = ("email or password must be wrong!!")
            return False
        self.warningMessage = ("login successfully")
        return True
    def checkRollcall(self):
        courseReq = self.rs.get(url = self.courseURL)
        if courseReq.content == b'':
            self.warningMessage = ("course URL must be wrong!!")
            return False
        courseReq.encoding = 'utf-8'
        regex_rollcallID = re.compile(r"var rollcall_id = \'(\w{0,})")
        rollcall_id = regex_rollcallID.search(courseReq.text).group(1)
        print(rollcall_id)
        if rollcall_id != "" and rollcall_id != self.rollcall_id:
            self.rollcall_id = rollcall_id
            self.rollcall()
        elif rollcall_id == "":
            self.warningMessage = ("No info yet "+time.ctime()[11:-5])
            return True
        
    def rollcall(self):
        """
        data: {
                user_id     : user_id,
                accessToken : accessToken,
                rollcall_id : rollcall_id,
                device      : 'WEB',
                lat         : user_latitude,
                lng         : user_longitude
            },
        """
        # assert self.rollcall_id != ""
        rollcallData = {
                    "user_id": self.userID,
                    "accessToken" : self.accessToken,
                    "rollcall_id" : self.rollcall_id,
                    "device": 'WEB',
                    "lat": self.lat,
                    "lng": self.lng
        }
        rollcallReq = self.rs.post(url = rollcallURL, data = rollcallData) #json??
        rollcallReq.encoding = 'utf-8'
        print(rollcallReq.text)
        if rollcallReq.json()["status"]:
            self.warningMessage = ("Successfully rollcall"+time.ctime()[11:-5])
            print(self.warningMessage)
            self.rollcall_id = ""
            return True
        else:
            self.warningMessage = (rollcallReq.json()["msg"]+time.ctime()[11:-5])
            print(self.warningMessage)            
            return False
    # def startRollcall(self,minute,hour=0,second=0):
    #     seconds = hour*3600+minute*60+second
    #     self.endTime = time.time()+seconds
        
    #     while time.time() <= self.endTime:
    #         self.checkRollcall()
    #         time.sleep(self.timePeriod)
    # def endTimeChecking(self):
    #     return time.time() <= self.endTime
    def checkIfInfoCorrect(self):
        if not self.login():
            return False
        if not self.checkRollcall():
            return False
        return True

# if __name__ == "__main__":
#     z = zuvio(mail = "b07901055@ntu.edu.tw",password="ray772425",courseURL="https://irs.zuvio.com.tw/student5/irs/rollcall/828938",lat=25.016168,lng=121.545303,timePeriod=20,minute=120)  
#     print(z.login())
#     z.checkRollcall()


class UI:
    def __init__(self,window,fileName):
        self.window = window
        self._task = None
        self.userInfo = {                        
                "email": "",\
                "password": "",\
                "url":"",\
                "lat":25.016168,\
                "lng":121.545303,
                "timePeriod":60,
        }
        self.fileName = fileName
        try: 
            with open(self.fileName,'rb') as f:
                self.userInfo = pickle.load(f)
        except:
            pass
        self.window.title('Zuvio Auto Rollcall')
        self.window.geometry('300x350')
        self.lbl_1 = tk.Label(self.window,text='email:',font=('Arial',12))
        self.lbl_1.grid(row=0,column=0)
        self.entry_1=tk.Entry(self.window)
        self.entry_1.insert(0,self.userInfo['email'])
        self.entry_1.grid(row=0,column=1)
        self.lbl_2 = tk.Label(self.window,text='password:',font=('Arial',12))
        self.lbl_2.grid(row=1,column=0)
        self.entry_2 = tk.Entry(self.window,show='*')
        self.entry_2.insert(0,self.userInfo['password'])
        self.entry_2.grid(row=1,column=1)
        self.lbl_3 = tk.Label(self.window,text='url of rollcall',font=('Arial',12))
        self.lbl_3.grid(row=2,column=0)
        self.entry_3 = tk.Entry(self.window)
        self.entry_3.insert(0,self.userInfo['url'])
        self.entry_3.grid(row=2,column=1)
        self.lbl_4 = tk.Label(self.window,text='time to refresh(sec)',font=('Arial',12))
        self.lbl_4.grid(row=3,column=0)
        self.scale_1 = tk.Scale(self.window,from_=10,to=600, length=150,resolution=20,orient='horizontal')
        self.scale_1.set(self.userInfo['timePeriod'])
        self.scale_1.grid(row=3,column=1,sticky=tk.E+tk.W)
        self.lbl_lat = tk.Label(self.window,text="latitude",font=('Arial',12))
        self.lbl_lat.grid(row=5,column=0)
        self.entry_lat = tk.Entry(self.window)
        self.entry_lat.insert(0,self.userInfo["lat"])
        self.entry_lat.grid(row=5,column=1)
        self.lbl_long = tk.Label(self.window,text="longitude",font=('Arial',12))
        self.lbl_long.grid(row=6,column=0)
        self.entry_long = tk.Entry(self.window)
        self.entry_long.insert(0,self.userInfo["lng"])
        self.entry_long.grid(row=6,column=1)
        self.btn_1 = tk.Button(self.window,text='go RollCall',command=self.startZuvio)
        self.btn_1.grid(row=9,column=0)
        self.btn_2 = tk.Button(self.window, text='exit',command=self.window.destroy)
        self.btn_2.grid(row=9,column=1)
        self.chkValue = tk.BooleanVar()
        self.chkValue.set(True)
        self.chkBox = tk.Checkbutton(self.window,text='remember me',var=self.chkValue)
        self.chkBox.grid(row=8)
        self.warningMessage = tk.Label(self.window,text='',font=('Arial',12))
        self.warningMessage.grid(row=11,columnspan=2)
    def startZuvio(self):
        if self.entry_1.get() == '':
            self.warningMessage['text']='missing: email is empty'
            return False
        elif self.entry_2.get() == '':
            self.warningMessage['text']='missing: password is empty'
            return False
        elif self.entry_3.get() == '':
            self.warningMessage['text']='missing:url is empty'
            return False
        try:
            self.userInfo['lat'] = float(self.entry_lat.get())
            self.userInfo['lng'] = float(self.entry_long.get())
        except:
            self.warningMessage['text'] = "lat and long must be number"
        self.userInfo['email'] =  self.entry_1.get()
        print("email",self.userInfo['email'])
        self.userInfo['password'] = self.entry_2.get()
        print("password",self.userInfo['password'])
        self.userInfo['url'] = self.entry_3.get()
        print("url",self.userInfo['url'])
        self.userInfo['timePeriod'] = self.scale_1.get()
        print("scale",self.userInfo['timePeriod'])
        self.warningMessage['text']=''
        if self.chkValue.get():
            with open(self.fileName,'wb') as f:
                pickle.dump(self.userInfo,f)
        self.z = zuvio(  self.userInfo["email"],
                    self.userInfo["password"],
                    self.userInfo["url"],
                    self.userInfo["lat"],
                    self.userInfo["lng"],
                    self.userInfo["timePeriod"])
        if not self.z.checkIfInfoCorrect():
            self.warningMessage['text'] = self.z.warningMessage
        self.warningMessage["text"] = self.z.warningMessage
        self.cancel_task()
        self.rollcallForever()
    def rollcallForever(self):
        self.z.checkRollcall()
        self.warningMessage["text"] = self.z.warningMessage
        self._task = self.window.after(self.userInfo["timePeriod"]*1000,self.rollcallForever)
    def cancel_task(self):
        if self._task is not None:
            self.window.after_cancel(self._task)
            self._task = None

if __name__ == "__main__":
    window = tk.Tk()
    u = UI(window,"userInfo.pckl")
    window.mainloop()

