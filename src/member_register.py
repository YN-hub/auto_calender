#sqlite
import sqlite3
import nfc 
import binascii
import datetime
import time
import pigpio
gpio_led2 = 27
gpio_buzz = 13
frq=5000
pi = pigpio.pi()
pi.set_mode(gpio_led2, pigpio.OUTPUT)
pi.set_mode(gpio_buzz, pigpio.OUTPUT)
#接続定義
clf = nfc.ContactlessFrontend('usb')  
print(clf)
#タグの取得
tag = clf.connect(rdwr={'on-connect': lambda tag: False})
#結果表示
print(str(tag.identifier))

# 接続。なければDBを作成する。
conn = sqlite3.connect('member.db')

# カーソルを取得
c = conn.cursor()
 
# テーブルを作成
try:
    c.execute('CREATE TABLE member_list  (id INTEGER,card_id BLOB, name varchar(1024),Entry datetime,Exit datetime)')

except sqlite3.OperationalError:
    print("")

pi.write(gpio_led2, 1)    # LED点灯
pi.hardware_PWM(gpio_buzz, frq, 500000)
time.sleep(0.1)            # 1秒待機
pi.write(gpio_led2, 0)    # LED消灯
pi.write(gpio_buzz, 0)    # LED消灯
time.sleep(0.1)            # 1秒待機
pi.write(gpio_led2, 1)    # LED点灯
pi.hardware_PWM(gpio_buzz, frq, 500000)
time.sleep(0.1)            # 1秒待機
pi.write(gpio_led2, 0)    # LED消灯
pi.write(gpio_buzz, 0)    # LED消灯
#ダブり検出
unique=1
sql = "select * from member_list"
c.execute(sql) # select文をexecute()に渡す
for row in c:  # レコードを出力する
    if row[1]==tag.identifier:
        unique=0
        print("This card already exists in the database.")
        break   
if unique==1:
    sql = 'SELECT count(*) FROM ' + 'member_list'
    #SQLを実行し、レコード数を得る
    c.execute(sql)
    result = c.fetchall()
    #結果は リスト、タプル型で出力される => [(5,)]
    record_max = result[0][0]
    # コミット
    name=input("名前を入れてください")
    # Insert実行
    c.execute(f"INSERT INTO member_list VALUES ({int(record_max+1)},?,'{str(name)}','{datetime.datetime(2022, 1, 25, 13, 00).isoformat()}','{datetime.datetime.now().isoformat()}')",[tag.identifier],)
    conn.commit()

 
# コネクションをクローズ
conn.close()
