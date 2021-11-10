from bs4 import BeautifulSoup as bs
import requests as rq
from selenium import webdriver
import time
import tkinter as tk
import pickle
url_login = "https://irs.zuvio.com.tw/irs/login"
# parameters user need to key in 
# set an ui or json file
my_dict = {'url':'','email':'','time_to_refresh':20,'password':''} 
# email = ""
# password = ""
# time_to_refresh = 20
window = tk.Tk()
# course_name = "防衛動員（67節）"
def getInfo():
    # global my_dict
    if entry_1.get() == '':
        warningMessage['text']='missing: email is empty'
        return False
    elif entry_2.get() == '':
        warningMessage['text']='missing: password is empty'
        return False
    elif entry_3.get() == '':
        warningMessage['text']='missing:url is empty'
        return False
    my_dict['email'] =  entry_1.get()
    print("email",my_dict['email'])
    my_dict['password'] = entry_2.get()
    print("password",my_dict['password'])
    my_dict['url'] = entry_3.get()
    print("url",my_dict['url'])
    my_dict['time_to_refresh'] = scale_1.get()
    print("scale",my_dict['time_to_refresh'])
    warningMessage['text']=''
    if chkValue.get():
        with open('userInfo.pckl','wb') as f:
            pickle.dump(my_dict,f)
    return True

    
# login
def login():
    if not getInfo():
        return
    driver = webdriver.Chrome()
    driver.get(url_login)
    email_input = driver.find_element_by_id('email')
    password_input = driver.find_element_by_id('password')
    login_button = driver.find_element_by_id('login-btn')
    email_input.send_keys(my_dict['email'])
    password_input.send_keys(my_dict['password'])
    login_button.click()
    rollcall(driver)
def rollcall(driver):
    global window
    print("scale",my_dict['time_to_refresh'])
    driver.get(my_dict['url'])
    PageSource = driver.page_source
    soup = bs(PageSource,'html.parser')
    result = soup.find("div",class_="i-r-footer-box")
    time_now = time.ctime()[11:-5]
    if result == None:
        print(time_now,"no info yet")
        warningMessage['text']=time_now+' no info yet'            
    else:
        if "已簽到" in result.text:
            warningMessage['text']=time_now+' rollcall successfully'
            driver.close()         
            return
        if "我到了" in result.text:
            driver.find_element_by_id("submit-make-rollcall").click()
            warningMessage['text'] = time_now+' click the button'
    window.after(my_dict['time_to_refresh']*1000,rollcall,driver)

if __name__ == "__main__":
    # rollcall()
    # global my_dict
    try:
        with open('userInfo.pckl','rb') as f:
            my_dict = pickle.load(f)
    except:
        pass
    window.title('Zuvio Auto Rollcall')
    window.geometry('300x200')
    lbl_1 = tk.Label(window,text='email:',font=('Arial',12))
    lbl_1.grid(row=0,column=0)
    entry_1=tk.Entry(window)
    entry_1.insert(0,my_dict['email'])
    entry_1.grid(row=0,column=1)
    lbl_2 = tk.Label(window,text='password:',font=('Arial',12))
    lbl_2.grid(row=1,column=0)
    entry_2 = tk.Entry(window,show='*')
    entry_2.insert(0,my_dict['password'])
    entry_2.grid(row=1,column=1)
    lbl_3 = tk.Label(window,text='url of rollcall',font=('Arial',12))
    lbl_3.grid(row=2,column=0)
    entry_3 = tk.Entry(window)
    entry_3.insert(0,my_dict['url'])
    entry_3.grid(row=2,column=1)
    lbl_4 = tk.Label(window,text='time to refresh(sec)',font=('Arial',12))
    lbl_4.grid(row=3,column=0)
    scale_1 = tk.Scale(window,from_=10,to=600, length=150,resolution=20,orient='horizontal')
    scale_1.set(my_dict['time_to_refresh'])
    scale_1.grid(row=3,column=1,sticky=tk.E+tk.W)
    btn_1 = tk.Button(window,text='go RollCall',command=login)
    btn_1.grid(row=6,column=0)
    btn_2 = tk.Button(window, text='exit',command=window.destroy)
    btn_2.grid(row=6,column=1)
    chkValue = tk.BooleanVar()
    chkValue.set(True)
    chkBox = tk.Checkbutton(window,text='remember me',var=chkValue)
    chkBox.grid(row=4)
    warningMessage = tk.Label(window,text='',font=('Arial',12))
    warningMessage.grid(row=5,columnspan=2)
    window.mainloop()
