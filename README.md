fb-crawler (fb 網路爬蟲) 
===
* 爬取使用者的"公開個人資料"
* 爬取使用者 "按讚的粉絲專頁"
* 爬取使用者 "打卡地點及打卡時間"
* 輸出 Json 格式
* 爬取後的網頁存於.\cache.
* (可選) 使用己登入的使用者設定檔,代替重複登入
* 配合資料庫。

### 執行環境
* Python 3.6

### 套件需求
* selenium
* bs4
* pymysql
* demjson
* json

### 安裝說明
* 本實驗使用的FB帳號語言需為 中文(香港) , 中文(台灣) 尚在測試

* 需登入有效的FB帳號才能爬取,請把config.json.dist更改名稱為config.json 且輸入FB帳號及密碼

* 也可使用己登入的使用者設定檔進行爬取


### 使用己登入的使用者設定檔進行爬取

Google Chrome:
```
1. 把browser.prepare_chrome(None) 的None 替換成對應的設定檔目錄
使用者設定檔位置: C:\Users\你的使用者名稱\AppData\Local\Google\Chrome\User Data

2. 注解browser.login_fb()
```

Firefox:
```
1. 把browser.prepare_firefox(None) 的None 替換成對應的設定檔目錄
使用者設定檔位置: %APPDATA%\Mozilla\Firefox\Profiles\xxxxxxxx.default

2. 注解browser.login_fb()

```

網頁檔案
---
爬蟲程式爬取網頁檔案後放置於 ".\cache"

再次啟動預設會從.\cache目錄讀取上次儲存的網頁檔案.

可清除.\cache 目錄下的檔案或停用快取以得最新更新


* 停用快取

把 main.py 中的
```
    if  browser.is_exist_in_cache(url):
        print("從快取中讀取 : {0}".format(re.sub(r'[^a-z0-9]', '', url) + '.html'))
        page_source = browser.read_cache(url)
    else :
        print("爬取: {0}".format(url))
        browser.nav(url)
        browser.scroll()
        page_source = browser.save()
```
修改成
```

        browser.nav(url)
        browser.scroll()
        page_source = browser.save()

```



範例
===


### 取得使用者公開資訊

    執行python main.py get_personal_information

 從目錄下的 user_fbid_example.json 輸入想要爬取的使用者fbid,
  取得使用者公開資訊,
  

  輸出至.\result 的 \\<使用者fbid>_get_personal_information_mobile.json
``` 
{
{
  "birthday": "2月13日",
  "bloodtype": "",
  "cname": "Tom (大明)",
  "current_city": "在 2004年搬到這裡",
  "education_data": [
    {
      "begin": null,
      "city": "",
      "end": null,
      "fbid": "109379529087796",
      "name": "National Chi Nan University",
      "type": "",
      "url": "/profile.php?id=109379529087796&refid=17"
    },
    {
      "begin": null,
      "city": "",
      "end": null,
      "fbid": "107977529234705",
      "name": "Pei Hwa High School",
      "type": "",
      "url": "/profile.php?id=107977529234705&refid=17"
    },
  ],
  "ename": "陳大明",
  "fbid": "1111111111",
  "gender": 1,
  "hometown": "澳門",
  "interested_in": "女性
  ",
  "other": "大明",
  "political_view": "Sluggish",
  "quotes": "",
  "relationship": "單身",
  "religious": "",
  "skills": "",
  "work_data": [
    {
      "begin": "2010-07-01T00:00:00",
      "city": "",
      "end": null,
      "fbid": "574486383011427",
      "name": "plantation manager",
      "position": "Kelantan",
      "url": "/profile.php?id=574486383011427&refid=17"
    },
    {
      "begin": null,
      "city": "",
      "end": null,
      "fbid": null,
      "name": "ZZZ有限公司",
      "position": "關丹",
      "url": "/ZZZ有限公司-533246270096282/?refid=17"
    }
  ]
  "year_overviews": ""
}
}
         

```

取得使用者按讚的粉絲專頁
---
從目錄下的 user_fbid_example.json 輸入想要爬取的使用者fbid,且取得他按讚的粉絲專頁

```
執行 python main.py get_fbuser_like_fbpage
```
  輸出至.\result 的 \<使用者fbid>_get_fbuser_like_fbpage.json

```
[
  {
    "fbid": "147793401951357",
    "name": "台灣藝術大學演藝廳",
    "url": "/profile.php?id=147793401951357"
  },
  {
    "fbid": "274262012584734",
    "name": "歷史上很有名的14張靈異照片（膽小者慎入)",
    "url": "/歷史上很有名的14張靈異照片膽小者慎入-274262012584734/"
  },
  {
    "fbid": "128803760549510",
    "name": "【精彩】 詭異的美女圖，誰能看出什麼？",
    "url": "/精彩-詭異的美女圖誰能看出什麼-128803760549510/"
  },
  {
    "fbid": null,
    "name": "Namewee 黃明志",
    "url": "/namewee/"
  }
]
```


取得打卡地點及打卡時間
---
* 注意: 過度使用本任務會被FB封鎖而不能瀏覽其他使用者的個人檔案(不影响其他功能),通常會24小時後會解除

從目錄下的 user_fbid_example.json 輸入想要爬取的使用者fbid,
```
執行 python main.py get_check_in_with_time
```
輸出至.\result 的 \<使用者fbid>_get_check_in_with_time.json

```
[
  {
    "date": "2019-04-01T00:00:00",
    "fbid": "",
    "name": "台中東協廣場",
    "url": "https://www.facebook.com/TaichungAseanSquare/"
  },
  {
    "date": "2019-03-01T00:00:00",
    "fbid": "193806997315897",
    "name": "中台襌寺",
    "url": "https://www.facebook.com/pages/%E4%B8%AD%E5%8F%B0%E8%A5%8C%E5%AF%BA/193806997315897"
  },
  {
    "date": "2019-02-01T00:00:00",
    "fbid": "187317121312866",
    "name": "万佛殿",
    "url": "https://www.facebook.com/pages/%E4%B8%87%E4%BD%9B%E6%AE%BF/187317121312866"
  },
  {
    "date": "2019-02-01T00:00:00",
    "fbid": "",
    "name": "Pantai Teluk Cempedak",
    "url": "https://www.facebook.com/pantaitelukcempedak/"
  }
 ]
```



取得粉絲專頁類型,店家坐標等資訊
---
從目錄下的 fbpage_fbid_example.json 輸入想要爬取的粉絲專頁fbid

```
執行 python main.py get_fbpage_informaton
```
輸出至.\result 的 <粉絲專頁fbid>_get_fbpage_informaton.json

```
{
  "fbid": "112048405474076",
  "name": "澳門科技大學",
  "blue_verification_badge": false,
  "lat": "22.151837141305",
  "lng": "113.56635783219",
  "likes": "2641",
  "offical_website": "http://www.must.edu.mo/",
  "type": [
    "學校",
    "高中及大學"
  ]
}
```



配合資料庫進行爬取
---
* 使用	MySQL 第 2 代 5.7


* 資料庫ER-Model :
https://www.dropbox.com/s/7w8cbji6zc7mo86/FBFD.pptx?dl=0

* 資料庫(包含Stored Procedure):檔案於專案目錄
.\db\fb.mwb 或 .\db\fb.sql

* 在config.json 中輸入連線資訊

* 於main.py中

取消注解
```
    fb_crawler.set_personal_information_mobile(fbid,data)
    fb_crawler.set_fbuser_like_fbpage_moblie(user_fbid, data)
    fb_crawler.set_check_in_with_time(user_fbid,data)
```
以及把
```
    fbids = read_from_json_file('user_fbid_example.json')
```
fbids
替換成從資料庫讀取的 fbid

TODO
---
* 支援台灣(中文)的FB帳號
* 以手機版爬取打卡地點及打卡時間減小被封鎖可能




