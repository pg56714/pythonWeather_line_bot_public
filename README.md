# Python Flask 架設 LINE BOT 天氣預報

串接氣象公開資料 API，再利用 Flask 建置 API 提供 `LINE BOT` 進行天氣預報。最後並部署到 `Render` 雲端伺服器平台。

## Getting Started

### Installation

此專案下載至桌面後，使用以下指令安裝必要套件。

```
pip install -r requirements.txt
```

### Running the Project

套件安裝成功後，從 LINE bot 提取 access_token、secret 輸入到程式碼內，輸入氣象公開資料 API 到程式碼內，再設定 Webhook URL ，即可開始進行天氣預報。

```
python run.py
```
