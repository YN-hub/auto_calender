from __future__ import print_function

import datetime
import os.path
import sqlite3
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import nfc
import time
import pigpio
import googleapiclient.discovery
import google.auth
gpio_led = 17
gpio_led2 = 27
gpio_buzz = 13
frq=5000
volume=80000 #500000:50%
pi = pigpio.pi()
pi.set_mode(gpio_led, pigpio.OUTPUT)
pi.set_mode(gpio_led2, pigpio.OUTPUT)
pi.set_mode(gpio_buzz, pigpio.OUTPUT)

start_delay_time=0.3



for i in frqs:
    pi.hardware_PWM(gpio_buzz, i, 100000)
    time.sleep(start_delay_time)
time.sleep(1)
pi.write(gpio_buzz, 0)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
while True:
    #接続定義
    clf = nfc.ContactlessFrontend('usb')   
    print(clf)
    #タグの取得
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})

    # 接続。なければDBを作成する。
    conn = sqlite3.connect('member.db')
    clf.close()
    # カーソルを取得
    c = conn.cursor()
    sql="select * from member_list "

    registered=0# 0 : 登録されていない , 1 : 登録されている
    returning=0 # 0 : 出勤,  1 : 帰宅
    c.execute(sql)
    for row in c:
        if row[1]==tag.identifier:
            registered=1
            if row[3]<row[4]:
                sql=f"update member_list set Entry = '{datetime.datetime.now().isoformat()}' where id = {row[0]}"
                c.execute(sql)
            else:
                returning=1
                sql=f"update member_list set Exit = '{datetime.datetime.now().isoformat()}' where id = {row[0]}"
                c.execute(sql)
                conn.commit()    
            break   
    if registered==0:
        pi.write(gpio_led2, 1)    # LED点灯
        pi.hardware_PWM(gpio_buzz, frq, volume)
        time.sleep(0.3)            # 1秒待機
        pi.write(gpio_led2, 0)    # LED消灯
        pi.write(gpio_buzz, 0)
        time.sleep(0.3)            # 1秒待機
        pi.write(gpio_led2, 1)    # LED点灯
        pi.hardware_PWM(gpio_buzz, frq, volume)
        time.sleep(0.1)            # 1秒待機
        pi.write(gpio_led2, 0)    # LED消灯
        pi.write(gpio_buzz, 0)    # LED消灯
        time.sleep(0.1)            # 1秒待機
        pi.write(gpio_led2, 1)    # LED点灯
        pi.hardware_PWM(gpio_buzz, frq, volume)
        time.sleep(0.1)            # 1秒待機
        pi.write(gpio_led2, 0)    # LED消灯
        pi.write(gpio_buzz, 0)    # LED消灯
        print("カードが登録されていません")
        conn.close()
    elif(returning==1):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        print("お疲れ様でした!")
        pi.write(gpio_led, 1)    # LED点灯
        pi.hardware_PWM(gpio_buzz, frq, volume)
        time.sleep(0.5)            # 3秒待機
        pi.write(gpio_led, 0)    # LED消灯
        pi.write(gpio_buzz, 0)    # LED消灯
        creds = None

        creds = google.auth.load_credentials_from_file('credential.json', SCOPES)[0]
        try:
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            page_token = None
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            entry_time=row[3]
            # calendarList.get()
            body = {
                # 予定のタイトル
                'summary': f'{row[2]}在室',
                # 予定の開始時刻
                'start': {
                    'dateTime': entry_time,
                    'timeZone': 'Japan'
                },
                # 予定の終了時刻
                'end': {
                    'dateTime': datetime.datetime.now().isoformat(),
                    'timeZone': 'Japan'
                },
            }
            event = service.events().insert(calendarId='calender_ID', body=body).execute()
            conn.close()

        except HttpError as error:
            print('An error occurred: %s' % error)
            conn.commit()        
            conn.close()
    else:
        print(f"{row[2]}さん こんにちは")
        pi.write(gpio_led, 1)    # LED点灯
        pi.hardware_PWM(gpio_buzz, frq, volume)
        time.sleep(0.3)            # 1秒待機
        pi.write(gpio_led, 0)    # LED消灯
        pi.write(gpio_buzz, 0)    # LED消灯
        time.sleep(0.3)            # 1秒待機
        pi.write(gpio_led, 1)    # LED点灯
        pi.hardware_PWM(gpio_buzz, frq, volume)
        time.sleep(0.3)            # 1秒待機
        pi.write(gpio_led, 0)    # LED消灯
        pi.write(gpio_buzz, 0)    # LED消灯
        conn.commit()
        conn.close()
pi.stop()
