# auto_calender

 半自動在室記録デバイス

## Description
 
 交通系ICおよび学生証を用いたコロナ対策用の入退室管理を半自動化するデバイスです。使用前にICカードと使用者の名前をデータベースに登録してください。 登録したICカードを入室時と退室時にかざすと、自動で在室記録がGoogle Calenderへアップロードされます。

## Usage
 
このデバイスを使用するにはいくつかステップを踏む必要があります。
※必要なデバイス
* Raspberry Pi (Ubuntu Server版)
* NFCカードリーダ（Sony PaSoRi, RC-S380）

### 1.Google Calender APIを有効化
 * Google Cloud Consoleに登録　＆　新しいプロジェクトを作成 
 * APIを有効化 （メニュー -> APIとサービス -> ライブラリ -> Google Calender API -> 有効にする）
 * OAuth同意　（メニュー -> APIとサービス -> OAuth同意画面 ）以下の内容で登録
 
 ユーザの種類：外部
 アプリ名：任意の名前
 テストユーザ：Google Cloud Consoleに登録したメールアドレス
 Scope：Google Calender API /auth/calender 
 
 * 認証情報を作成　（メニュー -> APIとサービス -> 認証情報　-> 認証情報を作成　-> サービスアカウント　-> "情報を入力" -> 完了）
 * 認証情報が記載されているJSONファイルを生成 （直前の手順で生成されたサービスアカウントをクリック）
 * 下の画像の赤線が引かれた部分をクリックして、"鍵を追加"をクリック　＆　JSONファイルをダウンロード
 
 ![説明](https://user-images.githubusercontent.com/82434854/162227903-491bf60a-a48a-4856-9f45-be6e198615da.png)

### 2.カレンダーへサービスアカウントを追加
 * 「1.Google Calender APIを有効化」でダウンロードした認証情報が記載されているJSONファイルの名前を"credential.json"に変更
 *  auto_calender.pyやmember_register.pyと同じ階層へJSONファイルを移動させる
 *  Google Calenderアプリを開き、[外部サイト](http://www.yahoo.co.jphttps://www.cdatablog.jp/entry/googlecalendarserviceaccount)の「3. サービスアカウントへのカレンダーの共有」に従ってサービスアカウントをカレンダーへ追加　

### 3.デバイスの使用
 * member_register.pyを実行しNFCリーダへタッチ　＆　名前を打ち込み 
 * auto_calender.pyを実行
## Options
いくつか追加実装可能な機能
* Raspberry Piの起動と同時にauto_calender.pyが実行されるようにする -> Raspberry Pi のターミナルで"crontab -e"を実行し、"@reboot python3 /home/pi/auto_calender.py"を追加
* Raspberry PiにつなぐLEDについて　-> 



## Overview
 
![自動カレンダー筐体写真](https://user-images.githubusercontent.com/82434854/162221117-39613e1f-f559-486d-8232-f0d229202083.jpg)
