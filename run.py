# -*- coding: UTF-8 -*-
# 氣象會員及權杖取得： https://opendata.cwb.gov.tw/userLogin
# 氣象公開資料API： https://opendata.cwb.gov.tw/dist/opendata-swagger.html
# Line 貼圖： https://developers.line.biz/en/docs/messaging-api/sticker-list/

from flask import Flask, request

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage

import requests

app = Flask(__name__)

# 替換為你的 LINE Bot 的 Channel Access Token 和 Channel Secret
channel_access_token = 'YOUR_CHANNEL_ACCESS_TOKEN'
channel_secret = 'YOUR_CHANNEL_SECRET'

line_bot_api = LineBotApi(channel_access_token)  # 確認 token 是否正確
handler = WebhookHandler(channel_secret)        # 確認 secret 是否正確


@app.route('/callback', methods=['POST'])
def callback():
    # 獲取 header 資訊中的 X-Line-Signature
    signature = request.headers['X-Line-Signature']
    # 取得收到的訊息內容
    body = request.get_data(as_text=True)

    try:
        # 綁定訊息回傳的相關資訊
        handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature', 400

    return 'callback_OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        # 取得 LINE 收到的文字訊息
        msg = event.message.text
        # 取得回傳訊息的 Token
        reply_token = event.reply_token

        # 抓天氣預報資料
        # https://opendata.cwb.gov.tw/api/v1/rest/datastore/xxx?Authorization=Your_token&locationName=
        url = "氣象公開資料API網頁" + msg
        headers = {'Accept': 'application/json'}
        data = requests.get(url, headers=headers)
        data = data.json()
        city = str(data['records']['location'][0]['locationName'])
        start = str(data['records']['location'][0]
                    ['weatherElement'][2]['time'][2]['startTime'])
        tempmin = str(data['records']['location'][0]['weatherElement']
                      [2]['time'][2]['parameter']['parameterName'])+"度"
        tempmax = str(data['records']['location'][0]['weatherElement']
                      [4]['time'][2]['parameter']['parameterName'])+"度"
        rain = str(data['records']['location'][0]['weatherElement']
                   [1]['time'][2]['parameter']['parameterName'])+"%"
        end = str(data['records']['location'][0]
                  ['weatherElement'][2]['time'][2]['endTime'])
        msg1 = '✨'+city+'✨\n'+start+"~\n"+end+"\n❄️最低溫是："+tempmin + \
            "，\n🔥最高溫是："+tempmax+"；\n💧降雨機率是:"+rain+'\n\n數據取自中央氣象局'

        # 判斷貼圖(降雨機率)
        if (rain > '50'):
            PID = 11537
            SID = 52002750
            # image1 = 'https://imgur.dcard.tw/CdUYfMih.jpg'
            # image2 = 'https://imgur.dcard.tw/CdUYfMih.jpg'
        if (rain == '50'):
            PID = 11537
            SID = 52002749
        if (rain < '50'):
            PID = 11537
            SID = 52002735
            # image1 = 'https://e.share.photo.xuite.net/h00889942/1ec167e/12844799/649636735_m.jpg'
            # image2 = 'https://e.share.photo.xuite.net/h00889942/1ec167e/12844799/649636735_m.jpg'

        reply_txt = TextSendMessage(msg1)
        reply_stk = StickerSendMessage(package_id=PID, sticker_id=SID)
        # 回傳訊息
        line_bot_api.reply_message(reply_token, [reply_txt, reply_stk])
    except:
        msg1 = '查無此縣市，請重新輸入!'
        line_bot_api.reply_message(reply_token, TextSendMessage(msg1))
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
