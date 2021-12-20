# Zuvio Auto Rollcall 自動點名(2021)
### required
- python3
- BeautifulSoup 
- requests
- selenium
- tkinter

可透過 pip install 或是 conda install -c等語法下載
- chrome webdriver
    - 找出chrome版本，根據版本下載對應webdriver

- 將webdriver與zuvioRollcall.py放在同個資料夾內即可
#### chrome version
![](https://i.imgur.com/kEYhxfi.png)

點選"關於Google Chrome"即可得知

![](https://i.imgur.com/7i1Tu6x.png)

如我現在版本為95.0.4638.69

### how to use
```
python zuvioRollcall.py
```
開啟後出現GUI介面

![](https://i.imgur.com/tHqj9ib.png)

- email: zuvio帳號的email
- password: zuvio帳號的密碼
- url to rollcall: 點名簽到的網址
    - 點入課名後點選點名簽到，將其網址複製下來貼上即可
- time to refresh: 更新速度，預設是20秒，最多是600秒
- 按下rollcall，下方會有提示字條(有無點名資訊、是否點到名)

然後就可以去睡覺了

### others
目前打算增加:
- 紀錄點名資訊
- 課程名稱-網址管理
- fake GPS

如有更新會即刻上傳

