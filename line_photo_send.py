from PIL import Image
import numpy as np
import picamera
import time
import requests
import urllib.parse as parse
import datetime


def take_photo(pixel_x, pixel_y, file_path):
    with picamera.PiCamera() as camera:
        camera.resolution = (pixel_x, pixel_y)  # 撮影する画像の縦横ピクセル 横x縦
        camera.framerate = 24  # フレームレート
        time.sleep(2)  # カメラのセットアップが終わるのを待つ
        camera.capture(file_path)


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


if __name__ == '__main__':
    file_path = '/home/---/Desktop/test.jpg'
    # 自分の環境のを貼ってください
    
    take_photo(1980, 1080, file_path) #解像度は任意で設定。これがraspi cam v1.3の最大値と思われる
    nowtm = str(datetime.datetime.now())
    message = "\n写真を撮りました\n時刻"+nowtm  # メッセージ内容
    image_path = file_path  # 画像データ
    result = send_notif(message, image_path)
    print(result)  # メッセージがが送れたかどうかの結果を表示
