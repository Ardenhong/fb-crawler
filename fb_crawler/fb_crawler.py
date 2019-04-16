from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
from datetime import datetime
import random
import time
import sys
import re
import json
import db
import demjson

location_str = 'Macau Taiwan 澳門 香港 臺北市 基隆市 新北市 連江縣 宜蘭縣 新竹市 新竹縣 桃園市 苗栗縣 臺中市 彰化縣 南投縣 嘉義市 嘉義縣 雲林縣 臺南市 高雄市 澎湖縣 金門縣 屏東縣 臺東縣 花蓮縣 其他地區 成功鎮 佳冬鄉 麥寮鄉 綠島鄉 蘭嶼鄉 田中鎮 社頭鄉 竹田鄉 萬丹鄉 三灣鄉 峨眉鄉 南庄鄉 南屯區 烏日區 西區 東區 太保市 中埔鄉 番路鄉 水上鄉 員林市 旗津區 小港區 南竿鄉 北竿鄉 莒光鄉 東引鄉 金城鎮 金沙鎮 金湖鎮 金寧鄉 烏坵鄉 宜蘭市 羅東鎮 礁溪鄉 員山鄉 冬山鄉 三星鄉 大同鄉 竹東鎮 新埔鎮 關西鎮 湖口鄉 芎林鄉 橫山鄉 北埔鄉 寶山鄉 尖石鄉 五峰鄉 苗栗市 卓蘭鎮 大湖鄉 公館鄉 銅鑼鄉 頭屋鄉 三義鄉 西湖鄉 造橋鄉 獅潭鄉 泰安鄉 彰化市 和美鎮 線西鄉 伸港鄉 秀水鄉 花壇鄉 芬園鄉 溪湖鎮 東石鄉 大村鄉 埔鹽鄉 埔心鄉 永靖鄉 二水鄉 北斗鎮 二林鎮 田尾鄉 埤頭鄉 芳苑鄉 大城鄉 竹塘鄉 溪州鄉 南投市 埔里鎮 草屯鎮 竹山鎮 集集鎮 名間鄉 鹿谷鄉 中寮鄉 魚池鄉 國姓鄉 水里鄉 信義鄉 仁愛鄉 斗六市 斗南鎮 虎尾鎮 西螺鎮 土庫鎮 北港鎮 古坑鄉 大埤鄉 莿桐鄉 林內鄉 二崙鄉 崙背鄉 東勢鄉 褒忠鄉 元長鄉 水林鄉 朴子市 大林鎮 民雄鄉 溪口鄉 新港鄉 六腳鄉 義竹鄉 鹿草鄉 竹崎鄉 梅山鄉 大埔鄉 阿里山鄉 屏東市 潮州鎮 長治鄉 麟洛鄉 九如鄉 里港鄉 鹽埔鄉 高樹鄉 萬巒鄉 內埔鄉 新埤鄉 崁頂鄉 南州鄉 琉球鄉 三地門鄉 霧臺鄉 瑪家鄉 泰武鄉 來義鄉 春日鄉 獅子鄉 關山鎮 鹿野鄉 池上鄉 海端鄉 延平鄉 鳳林鎮 玉里鎮 光復鄉 瑞穗鄉 富里鄉 萬榮鄉 卓溪鄉 馬公市 湖西鄉 白沙鄉 西嶼鄉 望安鄉 七美鄉 七堵區 暖暖區 仁愛區 信義區 東區 松山區 信義區 大安區 中山區 中正區 大同區 萬華區 文山區 南港區 內湖區 士林區 北投區 鹽埕區 三民區 新興區 前金區 苓雅區 前鎮區 金峰鄉 蘇澳鎮 頭城鎮 壯圍鄉 五結鄉 南澳鄉 竹北市 新豐鄉 苑裡鎮 通霄鎮 竹南鎮 後龍鎮 鹿港鎮 福興鄉 臺西鄉 四湖鄉 口湖鄉 布袋鎮 東港鎮 恆春鎮 枋寮鄉 新園鄉 林邊鄉 車城鄉 滿州鄉 枋山鄉 牡丹鄉 臺東市 卑南鄉 東河鄉 長濱鄉 太麻里鄉 大武鄉 達仁鄉 花蓮市 新城鄉 吉安鄉 壽豐鄉 豐濱鄉 秀林鄉 中正區 中山區 安樂區 北區 香山區 鼓山區 左營區 楠梓區 鳳山區 大寮區 大樹區 大社區 仁武區 鳥松區 岡山區 橋頭區 燕巢區 田寮區 阿蓮區 路竹區 湖內區 旗山區 美濃區 六龜區 甲仙區 杉林區 內門區 茂林區 桃源區 那瑪夏區 板橋區 三重區 中和區 永和區 新莊區 新店區 樹林區 鶯歌區 三峽區 汐止區 土城區 蘆洲區 五股區 泰山區 深坑區 石碇區 坪林區 平溪區 雙溪區 烏來區 中區 東區 南區 西區 北區 西屯區 北屯區 豐原區 東勢區 沙鹿區 后里區 神岡區 潭子區 大雅區 新社區 石岡區 外埔區 大肚區 霧峰區 太平區 大里區 和平區 新營區 鹽水區 白河區 柳營區 後壁區 東山區 麻豆區 下營區 六甲區 官田區 大內區 佳里區 學甲區 西港區 新化區 善化區 新市區 安定區 山上區 玉井區 楠西區 南化區 左鎮區 仁德區 歸仁區 關廟區 龍崎區 永康區 東區 北區 中西區 林園區 茄萣區 永安區 彌陀區 梓官區 淡水區 瑞芳區 林口區 三芝區 石門區 八里區 貢寮區 金山區 萬里區 大甲區 清水區 大安區 龍井區 七股區 將軍區 北門區 南區 安南區 安平區 梧棲區 桃園區 中壢區 大溪區 楊梅區 蘆竹區 龜山區 八德區 龍潭區 平鎮區 復興區 大園區 新屋區 觀音區 頭份市 烈嶼鄉 台中市 台南市 台北市 台東縣 台西鄉'

def is_ac_valid(driver):
    '''檢察FB 帳號有没有被封鎖
    Args:
        driver: selenium driver
    '''

    try:
        page_not_available = "//div[@class='UIFullPage_Container']/div[@class='pvl _4-do']/h2"
        WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.XPATH, page_not_available)))

        driver.get(
            "https://www.facebook.com/profile.php?id=1661203540&sk=map")
        WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.XPATH, page_not_available)))

        print("帳號被封鎖")
        return False
    except TimeoutException:
        # print (sys.exc_info()[0],sys.exc_info()[1])
        print("帳號可正常使用")
        return True

def login(driver, email, password):
    # 前往FB
    if driver.current_url.find("facebook") == -1:
        driver.get("https://www.facebook.com/")
    else:
        home_xpath = ".//a[@href='https://www.facebook.com/?ref=logo']"
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, home_xpath))).click()

    # 登入
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(email)
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "pass"))).send_keys(password)
    except TimeoutException:
        print("己登入")


    WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, "loginbutton"))).click()

    if is_ac_valid(driver) is False:
        print("帳號被封鎖")


def scroll(driver):
    # 使用JavaScript向下滾動,觸發ajax,載入更多內容

    while True:
        try:
            # 向下滾動,觸發ajax , 如己滾動到最底部則觸發 TimeoutException 且return
            more_item_xpath = "//div[@class='_3i9']/div[@class='_5h60 _30f']/img"
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, more_item_xpath)))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scrolling
        except TimeoutException as ex:
            #向下滾動,觸發ajax , 如己滾動到最底部則觸發 TimeoutException 且return
            try:
                WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.centeredIndicator')))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scrolling
            except TimeoutException as ex:
                print("scrolled")
                return


def fatch_fbid(str):
    '''取得url中取得該項目唯一的fbid
    Args:
        str: 超鏈結
    Returns:
        該粉絲専頁或項目的唯一fbid
    '''

    have_fbid = re.search(re.compile(r"\&id=(\d+)"), str)
    if have_fbid:
        fbid = have_fbid.groups()[0]
        return fbid

    have_fbid = re.search(re.compile(r"\?id=(\d+)"), str)
    if have_fbid:
        fbid = have_fbid.groups()[0]
        return fbid

    have_fbid = re.search(re.compile(r"\/(\d+)\/"), str)
    if have_fbid:
        fbid = have_fbid.groups()[0]
        return fbid

    return None


def conver_date(date):
    '''把時間從(\d+)年(\d+)月的格式轉成datetime
    Args:
        date: string 格式的時間
    Returns:
        datetime
    '''

    if not date:
        return None
    elif date.find('現在') >= 0:
        return None

    match_year_month = re.match(re.compile(r"(\d+)年(\d+)月"), date)
    match_year = re.match(re.compile(r"(\d+)年"), date)

    if (match_year_month):
        year = match_year_month.groups()[0]
        month = match_year_month.groups()[1]
        return datetime.strptime('{0} {1} 1'.format(year, month), '%Y %m %d')

    if (match_year):
        year = match_year.groups()[0]
        return datetime.strptime('{0} 1 1'.format(year), '%Y %m %d')


def short_sleep():
    second = 2 + random.uniform(1, 4)
    print('休息{0}秒'.format(second))

    time.sleep(second)

def long_sleep():
    second = (8 + random.uniform(2, 4))
    print('休息{0}秒'.format(second))

    time.sleep(second)




def get_my_friends(page_source):
    '''從我的朋友頁面取得所有我的朋友名單
    Args:
        page_source: 網頁頁面

    '''
    soup = bs(page_source, 'html.parser')
    count = 0
    errorCount = 0

    for li in soup.findAll('li', class_="_698"):
        try:
            block = li.find('div', class_="fsl fwb fcb")

            pageName = block.text
            pageFBID = demjson.decode(block.a["data-gt"])["engagement"]["eng_tid"]
            print(pageName, pageFBID)
            count += 1

        except KeyError as e:
            print(sys.exc_info()[0], sys.exc_info()[1])
            errorCount += 1
            # raise e
        except UnicodeEncodeError:
            print("except UnicodeEncodeError")

    print("共{0}筆!\n Error數:{1}".format(count, errorCount))


def get_all_fbuser_fbid(day):
    '''從資料庫取得資料庫內的所有使用者Fbid
    Returns:
        fbids:使用都的fbid 的list
    '''
    # time_pointer = datetime.datetime.now() - datetime.timedelta(days=day)
    fbids = db.exec('select fbid from fbuser')

    tmp = []
    for fbid in fbids:
        tmp.append(fbid[0])
    fbids = tmp

    return fbids


def get_check_in_with_time(user_fbid, page_source):
    '''獲取頁面內所有使用者的打卡地點及打卡時間
    Args:
        user_fbid: 使用者唯一的fbid
        page_source:頁面
    Returns:
        output : 包含使用者打卡地點資料的list
     '''

    soup = bs(page_source, 'html.parser')
    elm_collection = soup.select('._gx6._agv')

    output = []
    for elm in elm_collection:
        # 指標指向 標題 和 目標粉專連結
        elm_pointer = elm.select_one('._gx7')
        url = elm_pointer['href']
        name = elm_pointer.text
        fbid = ''

        # 指標指向 日期和發文連結
        elm_pointer = elm.select_one('._1fs8').select_one('a')
        if (elm_pointer):
            date = elm_pointer.text.replace('在 ', '').replace('造訪過', '').replace('瀏覽過', '')
            date = conver_date(date)
            elm_post_url = elm_pointer['href']
        else:
            date = ''
            elm_post_url = ''

        have_fbid = re.search(re.compile(r"\/(\d+)"), url)
        if have_fbid:
            fbid = have_fbid.groups()[0]

        data = {
            'fbid' : fbid,
            'url' : url,
            'name' : name,
            'date' :date
        }

        output.append(data)

    return output

def set_check_in_with_time(user_fbid,input_data):
    '''把使用者打卡地點及打卡時間上傳到資料庫
    Args:
        user_fbid: 使用者唯一的fbid
        input_data:包含使用者打卡地點資料的list
     '''

    for data in input_data:
        try:
            # 取得user 的 Primary Key
            fbuser_pk = db.exec('select id from fbuser '
                                'where fbid = %s', [user_fbid])
            if not fbuser_pk:
                print('{0} Fb user pk not find'.format(fbuser_pk))
                return

            # 把資料於到粉絲専業的table 中
            fbpage_pk = db.exec('call add_fbpage(%s)', data['name'])
            db.exec('update fbpage set fbid = %s ,url = %s where id = %s ;', [data['fbid'], data['url'], fbpage_pk])


            # 建立user 於何時就讀的關聯
            fbuser_has_check_in = db.exec('select 1 from fbuser_has_fbpage '
                                          'where fbuser_id = %s and fbpage_id = %s', [fbuser_pk, fbpage_pk])

            date = conver_date(data['date'])
            if not fbuser_has_check_in:
                db.exec('insert into fbuser_has_fbpage(fbuser_id,fbpage_id,type,ctype,begin)'
                        ' values (%s,%s,%s,%s,%s)', [fbuser_pk, fbpage_pk, 'checkin', '打卡', date])

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

            print('++++++++++++++++++++++++++++++++++++++++')
            print(data)
            print('++++++++++++++++++++++++++++++++++++++++')

    db.commit()


def get_fbpage_informaton(page_source):
    '''獲取粉絲專頁內的詳細資訊
    Args:
        user_fbid: 粉絲專頁唯一的fbid
        page_source:頁面
    Returns:
    '''

    lat = ''
    lng = ''
    fbid = ''
    type = ''
    offical_website = ''
    name = ''
    blue_verification_badge = False
    likes = 0

    soup = bs(page_source, 'html.parser')

    type_elm = soup.select_one('img[src="https://static.xx.fbcdn.net/rsrc.php/v3/y7/r/3OfQvJdYD_W.png"]').parent
    if type_elm :
        type = type_elm.text.split(' · ')

    offical_website_elm = soup.select_one('img[src="https://static.xx.fbcdn.net/rsrc.php/v3/yN/r/aE7VLFYMYdl.png"]').parent
    if type_elm :
        offical_website = offical_website_elm.text

    blue_verification_badge_elm = soup.select_one('img[src="https://static.xx.fbcdn.net/rsrc.php/v3/yN/r/ZRwcHdL-Tur.png"]')
    if blue_verification_badge_elm :
        blue_verification_badge = True

    likes_elm = soup.select_one('[style="font-size: 14px;font-weight: 400;line-height: 16px;color: #606770"]')
    if likes_elm :
        likes = re.search(re.compile(r"(\d+)"), likes_elm.text.replace(',','')).groups()[0]



    name_elm = soup.select_one('[data-sigil="MBackNavBarClick"]')
    if name_elm :
        name = name_elm.text.replace(' - 首頁','')

    fbid_elm = soup.select_one('a[rel = "async"]')
    if fbid_elm :
        fbid = fatch_fbid(fbid_elm['href'])

    geog_elm = soup.select_one('.profileMapTile')
    if geog_elm:
        landscape_url = demjson.decode(geog_elm['data-store'])['landscapeURL']

        lat = re.findall("\d+\.\d+", landscape_url)[0]
        lng = re.findall("\d+\.\d+", landscape_url)[1]

    data = {
        'fbid' : fbid,
        'offical_website' : offical_website,
        'name' : name,
        'type' :type,
        'lat' :lat,
        'lng' :lng,
        'blue_verification_badge' :blue_verification_badge,
        'likes' :likes,
    }
    

    

    return data

def get_fbuser_like_fbpage_moblie(user_fbid, page_source):
    '''在手機版網頁下,獲取使用者按讚的項目
    Args:
        user_fbid: 使用者唯一的fbid
        page_source:頁面
    Returns:
        output : 包含使用者按讚粉絲専頁資料的list
    '''

    soup = bs(page_source, 'html.parser')



    elm_collection = soup.select('._1a5p > a')

    output = []
    for elm in elm_collection:
        url = elm['href']
        name = elm.select_one('i')['aria-label']
        fbid = None

        have_fbid = re.search(re.compile(r"-(\d+)\/"), url)
        if have_fbid:
            fbid = have_fbid.groups()[0]
        else:
            fbid =  fatch_fbid(url)


        data = {
            'fbid' : fbid,
            'url' : url,
            'name' : name,
        }

        output.append(data)

    return output


def set_fbuser_like_fbpage_moblie(user_fbid,input_data):
    '''把使用者按讚粉絲専頁的資料上傳到資料庫
    Args:
        user_fbid: 使用者唯一的fbid
        input_data:包含使用者按讚粉絲専頁資料的list
     '''


    for data in input_data:
        try:
            fbuser_pk = db.exec('select id from fbuser '
                                'where fbid = %s', [user_fbid])
            if not fbuser_pk:
                print('{0} Fb user pk not find'.format(fbuser_pk))
                return


            fbpage_pk = db.exec('call add_fbpage(%s)', data['name'])
            if data['fbid']:
                db.exec('update fbpage set fbid = %s ,url = %s where id = %s ;', [data['fbid'], data['url'], fbpage_pk])


            # 建立user 於何時就讀的關聯
            fbuser_has_like = db.exec('select 1 from fbuser_has_fbpage '
                                          'where fbuser_id = %s and fbpage_id = %s', [fbuser_pk, fbpage_pk])

            # TODO year_graduation
            if not fbuser_has_like:
                db.exec('insert into fbuser_has_fbpage(fbuser_id,fbpage_id,type,ctype)'
                        ' values (%s,%s,%s,%s)', [fbuser_pk, fbpage_pk, 'like', '按讚'])

        except:
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

            print('++++++++++++++++++++++++++++++++++++++++')
            print(input_data)
            print('++++++++++++++++++++++++++++++++++++++++')

    db.commit()


def get_personal_information_mobile(user_fbid, page_source):
    '''在手機版網頁下,獲取使用者的個人資訊
    Args:
        user_fbid: 使用者唯一的fbid
        page_source:頁面
    Returns:
        output : 包含使用者資料的list
    '''
    soup = bs(page_source, 'html.parser')
    
    #=================================================================================================================
    # 學歷
    #=================================================================================================================
    # 篩選條件 : div 的child 為 a
    edu_nodes = []
    for node in soup.select('#education div > a '):
        node = node.parent
        edu_nodes.append(node)

    education_data = []
    for node in edu_nodes:
        edu_year = ''
        edu_city = ''
        edu_name = ''
        edu_fbid = ''
        edu_type = ''
        edu_year_begin = None
        edu_year_end = None
        edu_url=''
        
        # 抓取學校官方粉絲專頁
        if (node.select('span > a')):
            edu_url = node.select(' span > a')[0]['href']
            edu_fbid = fatch_fbid(edu_url)
            edu_name = node.select(' span > a')[0].text

        # 解析使用者於何時就讀
        detail_info = node.select(' div > span')
        for info in detail_info:
            info = info.text
            if info.find('大專院校') >= 0 or info.find('高中') >= 0 or info.find('國中') >= 0 or info.find('國小') >= 0:
                edu_type = info
            elif re.match(re.compile(r"(\d+)年"), info):
                edu_year = info


        # 把年份從中文轉換成datetime
        if edu_year:
            graduation = re.match(re.compile(r"畢業於 (\d+) 年"), info)
            if graduation:
                graduation_year = graduation.groups()[0]
                work_year_end = datetime.strptime('{0} 6 30'.format(graduation_year), '%Y %m %d')
            else:
                if edu_year.find(' ~ ') >= 0:
                    edu_year_begin = conver_date(edu_year.split(' ~ ')[0])
                    edu_year_end = conver_date(edu_year.split(' ~ ')[1])
                else:
                    edu_year_begin = None
                    edu_year_end = None

        
        data = {
            'fbid':edu_fbid,
            'name':edu_name,
            'begin':edu_year_begin,
            'end':edu_year_end,
            'city':edu_city,
            'type':edu_type,
            'url':edu_url
        }

        education_data.append(data)

    #=================================================================================================================
    # 工作經歷
    #=================================================================================================================
    # 篩選條件 : div 的child 為 a
    work_nodes = []
    for node in soup.select('#work div > a'):
        node = node.parent
        work_nodes.append(node)

    work_data = []
    for node in work_nodes:
        work_city = ''
        work_year = ''
        work_fbid = ''
        work_position = ''
        work_year_begin = None
        work_year_end = None
        

        # 抓取工作地點的官方粉絲專頁
        if (node.select('span > a')):
            work_url = node.select('a')[0]['href']
            work_fbid = fatch_fbid(work_url)

        # 判斷其餘資訊的meta data
        info_collection = []
        for info in node.select('span'):
            info_collection.append(info.text)

        work_name = info_collection.pop(0)

        for info in info_collection:
            if len(info) == 0:
                continue

            if re.match(re.compile(r"(\d+)年"), info):
                work_year = info
                continue

            if location_str.find(info) != -1:
                work_city = info
                continue

            work_position = info

        # 日期格式轉換
        if work_year:
            for split_str in [' ~ ',' - ']:
                if work_year.find(split_str) >= 0:
                    work_year_begin = conver_date(work_year.split(split_str)[0])
                    work_year_end = conver_date(work_year.split(split_str)[1])
                    break
        else:
            work_year_begin = None
            work_year_end = None

        data ={
            'fbid' : work_fbid,
            'name' :work_name,
            'position': work_position,
            'begin':work_year_begin,
            'end':work_year_end,
            'city':work_city,
            'url':work_url
        }

        work_data.append(data)


    #=================================================================================================================
    # 個人資料
    #=================================================================================================================
    # 他住過的地方
    current_city = ''
    hometown = ''
    birthday = ''
    bloodtype = ''
    gender = None
    religious = ''
    political_view = ''
    skills = ''
    relationship = ''
    other = ''
    quotes = ''
    interested_in = ''
    cname = ''
    ename = ''
    year_overviews = ''
    
    # 現居城市
    live_row = soup.select("#living tr")
    if (live_row):
        if (len(live_row) >= 1):
            current_city = live_row[1].select('a')[0].text

        if (len(live_row) >= 2):
            hometown = live_row[1].select('a')[0].text

    # 生活要事
    if (soup.select('#year-overviews')):
        year_overviews = soup.select('#year-overviews')[0].text

    # 專業技能
    if (soup.select_one('#skills')):
        skills = soup.select_one('#skills').text

    # relationship
    if (soup.select_one('#relationship')):
        if soup.select_one('#relationship tbody') :
            title = soup.select_one('#relationship tbody').text
            relationship = soup.select_one('#relationship').text.replace(title, '')
        else :
            relationship = soup.select_one('#relationship').text

    # 名言
    if (soup.select_one('#bio')):
        if soup.select_one('#bio tbody'):
            bio_title = soup.select_one('#bio tbody').text
            bio = soup.select_one('#bio').text
            bio = bio.replace(bio_title, '')
        else :
            bio = soup.select_one('#bio').text
        quotes = bio

    # 姓名
    selector = 'span > strong'
    if (soup.select_one(selector)):
        name_elm = soup.select_one(selector)
        cname = name_elm.text.replace(ename, '')
        ename_elm = name_elm.select_one('span')
        if ename_elm:
            ename = ename_elm.text

    # 透過標題的關鍵字找到他對應的變數
    row_with_title = soup.select('div[title]')
    for node in row_with_title:
        title = node['title']
        if node.select_one('a'):
            text = node.select_one('a').text
        else:
            text = node.select('td > div')[1].text.replace(title, '')
        if (title.find('生日') >= 0):
            birthday = text
        elif(title.find('血型') >= 0):
            bloodtype = text
        elif(title.find('戀愛性向') >= 0):
            interested_in = text
        elif(title.find('性別') >= 0):
            if text.find('男') >= 0:
                gender = 1
            elif text.find('女') >= 0:
                gender = 0
            else:
                gender = None
        elif (title.find('宗教信仰') >= 0):
            religious = text
        elif (title.find('政治立場') >= 0):
            political_view = text
        elif (title.find('其他') >= 0):
            other = text

    user_info = {
        'fbid':user_fbid,
        'current_city' : current_city,
        'hometown' : hometown,
        'year_overviews' : year_overviews,
        'skills' : skills,
        'relationship' : relationship,
        'quotes' : quotes,
        'cname' : cname,
        'ename' : ename,
        'birthday' : birthday,
        'bloodtype' : bloodtype,
        'interested_in' : interested_in,
        'gender' : gender,
        'religious' : religious,
        'political_view' : political_view,
        'other' : other,
        'education_data':education_data,
        'work_data':work_data
    }

    return user_info

def set_personal_information_mobile(user_fbid,input_data):
    '''把使用者資料上傳到資料庫
    Args:
        user_fbid: 使用者唯一的fbid
        input_data:包含使用者資料的list
    '''
    fbuser_pk = db.fetch_one('select id from fbuser where fbid = %s', [user_fbid])
    if not fbuser_pk:
        print('{0} Fb user pk not find'.format(fbuser_pk))
        return

    if input_data['education_data'] :
        for data in input_data['education_data']:
            if data['type'] and data['type'] != '':
                fbpage_pk = db.fetch_one('call add_fbpage_with_type(%s,%s)', [data['name'], data['type']])
            else:
                fbpage_pk = db.fetch_one('call add_fbpage(%s)', [data['name']])

            if data['fbid']:
                db.exec('update fbpage set fbid = %s ,url = %s where id = %s ;', [data['fbid'], data['url'], fbpage_pk])

            # 建立user 於何時就讀的關聯
            fbuser_has_education_exist = db.exec('select 1 from fbuser_has_fbpage '
                                                 'where fbuser_id = %s and fbpage_id = %s', [fbuser_pk, fbpage_pk])

            # TODO year_graduation
            if not fbuser_has_education_exist:
                db.exec('insert into fbuser_has_fbpage(fbuser_id,fbpage_id,type,ctype,begin,end)'
                        ' values (%s,%s,%s,%s,%s,%s)', [fbuser_pk, fbpage_pk, 'edu', '學歷', data['begin'], data['end']])

    if input_data['work_data']:
        for data in input_data['work_data']:
            fbpage_pk = db.fetch_one('call add_fbpage(%s)', [data['name']])
            if data['fbid']:
                db.exec('update fbpage set fbid = %s ,url = %s where id = %s ;', [data['fbid'], data['url'], fbpage_pk])


            try:
                # 建立user 於何時就讀的關聯
                fbuser_has_work_exist = db.exec('select 1 from fbuser_has_fbpage '
                                                'where fbuser_id = %s and fbpage_id = %s', [fbuser_pk, fbpage_pk])
                # TODO year_graduation
                if not fbuser_has_work_exist:
                    db.exec('insert into fbuser_has_fbpage(fbuser_id,fbpage_id,type,ctype,begin,end,postion)'
                            ' values (%s,%s,%s,%s,%s,%s,%s)',
                            [fbuser_pk, fbpage_pk, 'work', '工作經歷', data['begin'], data['end'], data['position']])

            except:
                print(sys.exc_info()[0])
                print(sys.exc_info()[1])

                print('++++++++++++++++++++++++++++++++++++++++')
                print(input_data['work_data'])
                print('++++++++++++++++++++++++++++++++++++++++')



    try:
        db.exec("update fbuser set  gender = %s"
                ", hometown = %s, relationship = %s, birthday = %s, ename = %s, cname = %s,"
                " bloodtype = %s, last_update = %s, current_city =%s where id = %s",
                [input_data['gender'], input_data['hometown'], input_data['relationship'], input_data['birthday']
                    , input_data['ename'], input_data['cname'], input_data['bloodtype'],
                 datetime.now(), input_data['current_city'], fbuser_pk])

        db.exec('update fbuser_ext set  religious = %s, political_view = %s, other = %s, quotes = %s '
                'where fbuser_id = %s', [input_data['religious'], input_data['political_view'], input_data['other'],
                                         input_data['quotes'], fbuser_pk])
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

        print(input_data)

    db.commit()

