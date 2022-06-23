from pickle import NONE
import requests
import urllib.parse as parse
import datetime


def send_notif(message, image_path=""):
  
    token = '---'  # LINE Notifyで発行されたトークン
    # 自分の環境のを貼ってください
    
    url = 'https://notify-api.line.me/api/notify'  # LINE NotifyのAPIのURL
    send_data = {'message': message}  # メッセージ
    headers = {'Authorization': 'Bearer ' + token}  # トークン名
    if image_path != "":
        files = {'imageFile': open(image_path, 'rb')}  # 画像ファイルのオープン
        res = requests.post(url,
                            data=send_data,
                            headers=headers,
                            files=files)
    else:
        res = requests.post(url,
                            data=send_data,
                            headers=headers)
    return res


nowtm = str(datetime.datetime.now())
message = "\n写真を撮りました\n時刻"+nowtm  # メッセージ内容

image_path = '/Users/---/Desktop/---/---/qrcode.png'  # 画像データ
# 自分の環境のを貼ってください

result = send_notif(message)
print(result)  # メッセージがが送れたかどうかの結果を表示
