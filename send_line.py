# 2022/06/22 gas python_hub deploy version 19

import requests


def send_line(message):
    url = "https://script.google.com/macros/s/---/exec"
    #gasのウェブアプリURLを貼り付け
    param = {
        "app": "line_send",
        "to": "---",
        # LINEのuserIDをtoへ貼り付け
        "message": message
    }
    res = requests.get(url, params=param)
    return res.text


print(send_line("hello python"))
