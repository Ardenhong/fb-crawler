from selenium import webdriver
import sys
import os
import codecs  # write to file
import re
from fb_crawler import fb_crawler
import json
import demjson


class Url_manager:
    '''管理不同任務的爬取Url
    '''
    def __init__(self):
        self.version = 'desktop'

    def use_mobile_version(self):
        self.version = 'mobile'

    def use_desktop_version(self):
        self.version = 'desktop'

    # 打卡地點
    def check_in_url(self,fbid):

        if self.version == 'desktop':
            url = 'https://www.facebook.com/profile.php?id={0}&sk=map'
            return url.format(fbid)
        else :
            print('無手機版爬蟲')

    # 打卡地點及時間
    def get_check_in_with_time_url(self,fbid):
        if self.version == 'desktop' :
            url = 'https://www.facebook.com/profile.php?id={0}&sk=places_recent'
            return url.format(fbid)
        else :
            print('無手機版爬蟲')

    # "關於" 頁面
    def get_personal_information_url(self,fbid):
        if self.version == 'desktop':
            print('無電腦版爬蟲')
        else :
            url = 'https://m.facebook.com/profile.php?v=info&lst=1326038533%3A1400534645%3A1549367704&id={0}&refid=17'
            return url.format(fbid)

    # 按讚的項目
    def get_fbuser_like_fbpage_url(self,fbid):
        if self.version == 'desktop':
            print('無電腦版爬蟲')
        else:
            url = 'https://m.facebook.com/timeline/app_collection/?collection_token={0}%3A2409997254%3A96'
            return url.format(fbid)

    def get_fbpage_informaton_url(self,fbid):
        if self.version == 'desktop':
            print('無電腦版爬蟲')
        else:
            url = 'https://m.facebook.com/{0}'
            return url.format(fbid)


class Browser:
    def __init__(self):
        self.driver = ''
        self.filePath = ".\\cache\\"
        self.current_url = ''


    def login_fb(self):
        # 登入到FB
        f = open('config.json', 'r')
        config = json.load(f)

        fb_crawler.login(self.driver,config['fbac']['username'],config['fbac']['password'])

    def nav(self, url):
        # 瀏覽目標網頁
        self.current_url = url
        self.driver.get(url)

    def scroll(self):
        # 使用JavaScript向下滾動,觸發ajax,載入更多內容
        fb_crawler.scroll(self.driver)

    def prepare_firefox(self,path):
        # 設定firefox的profile 位置且使用firefox 作為瀏覽器

        if (self.driver == ''):
            if path :

                profile = webdriver.FirefoxProfile(path)
                # Handle notifications
                profile.set_preference('permissions.default.desktop-notification', 1)
                self.driver = webdriver.Firefox(profile, executable_path=r'.\src\geckodriver.exe')
            else :
                profile = webdriver.FirefoxProfile()
                # Handle notifications
                profile.set_preference('permissions.default.desktop-notification', 1)
                self.driver = webdriver.Firefox(profile,  executable_path=r'.\src\geckodriver.exe')


    def prepare_chrome(self,path):
        # 設定chrome的profile 位置且使用chrome 作為瀏覽器
        if (self.driver == ''):
            # .\\browser_profile\\chrome\\"+profile_name

            # Handle notifications
            options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications": 2}
            options.add_experimental_option("prefs", prefs)

            # 程式結束時不關閉chrome
            options.add_experimental_option("detach", True)

            if path :
                options.add_argument("user-data-dir="+path)  # Path to your chrome profile
                driver = webdriver.Chrome(executable_path=r'.\src\chromedriver.exe', chrome_options=options)
                self.driver = driver

            else :
                driver = webdriver.Chrome(executable_path=r'.\src\chromedriver.exe', chrome_options=options)
                self.driver = driver

    def save(self):
        # 把目前網頁寫入到cache , 且回傳page_source
        url = self.current_url
        page_source = self.driver.page_source
        error_collection = ['無法顯示你所要求的頁面。有可能是暫時無法使用、損壞的連結或是你沒有瀏覽此頁的權限。', '你暫時被禁止使用此功能']

        for error in error_collection:
            if (page_source.find(error) >= 0):
                print(error)

        text_file = codecs.open(self.get_cache_path(url), "w", "utf-8")
        text_file.write(page_source)
        text_file.close()

        return page_source

    def read_cache(self, file_url):
        page_source = codecs.open(self.get_cache_path(file_url), "r", "utf-8")
        page_source = page_source.read()
        return page_source

    def get_cache_path(self, url):
        return self.filePath + re.sub(r'[^a-z0-9]', '', url) + '.html'

    def is_exist_in_cache(self, url):
        file_exist = os.path.isfile(self.get_cache_path(url))
        if (file_exist):
            file_size = os.stat(self.get_cache_path(url))
            if (file_exist and file_size):
                return True
        else:
            return False



class Task:
    def __init__(self):
        pass

    # 爬取使用者的公開資訊 (手機版FB)
    # 針對firefox設計,請使用browser.prepare_firefox
    def get_personal_information(self,fbids):
        browser = Browser()
        browser.prepare_firefox(None)
        browser.login_fb()

        for fbid in fbids:
            url_obj = Url_manager()
            url_obj.use_mobile_version()
            url = url_obj.get_personal_information_url(fbid)

            if  browser.is_exist_in_cache(url):
                print("從快取中讀取 : {0}".format(re.sub(r'[^a-z0-9]', '', url) + '.html'))
                page_source = browser.read_cache(url)
            else :
                print("爬取: {0}".format(url))
                browser.nav(url)
                browser.scroll()
                page_source = browser.save()

            data =  fb_crawler.get_personal_information_mobile(fbid,page_source)

            write_json_file('./result/',fbid+'_'+'get_personal_information_mobile',data)


            print(data)

            # 把資料寫入到資料庫
            # fb_crawler.set_personal_information_mobile(fbid,data)


    # 爬取使用者按讚的項目 (手機版FB)
    # 使用手機版減低被鎖可能
    # 針對chrome設計,請使用browser.prepare_chrome
    # PS:firefox 版本按讚的項目會變少
    def get_fbuser_like_fbpage(self,fbids):
        browser = Browser()
        browser.prepare_chrome(None)
        browser.login_fb()

        i = 0
        for user_fbid in fbids:
            url_obj = Url_manager()
            url_obj.use_mobile_version()
            url = url_obj.get_fbuser_like_fbpage_url(user_fbid)

            if  browser.is_exist_in_cache(url):
                print("從快取中讀取 : {0}".format(re.sub(r'[^a-z0-9]', '', url) + '.html'))
                page_source = browser.read_cache(url)
            else :
                print("爬取: {0}".format(url))
                browser.nav(url)
                browser.scroll()
                page_source = browser.save()


            if page_source:
                data = fb_crawler.get_fbuser_like_fbpage_moblie(user_fbid,page_source)
                print(data)

                # 把資料寫入到資料庫
                # fb_crawler.set_fbuser_like_fbpage_moblie(user_fbid, data)
                write_json_file('./result/',user_fbid+'_'+'get_fbuser_like_fbpage_moblie',data)

            else :
                print('該用戶不開放 說讚的項目')



            i += 1
            if i % 20 == 0:
                print('第{0}筆'.format(i))

    # 爬取使用者的打卡地點及打卡時間 (電腦版)
    # 手機版無打卡時間所以使用電腦版FB
    # 針對firefox設計,請使用browser.prepare_firefox
    def get_check_in_with_time(self,fbids):
        browser = Browser()
        browser.prepare_firefox(None)
        browser.login_fb()

        i = 0
        for user_fbid in fbids:
            url_obj = Url_manager()
            url_obj.use_desktop_version()
            url = url_obj.get_check_in_with_time_url(user_fbid)

            if  browser.is_exist_in_cache(url):
                print("從快取中讀取 : {0}".format(re.sub(r'[^a-z0-9]', '', url) + '.html'))
                page_source = browser.read_cache(url)
            else :
                print("爬取: {0}".format(url))
                browser.nav(url)
                browser.scroll()
                page_source = browser.save()

            data = fb_crawler.get_check_in_with_time(user_fbid,page_source)
            write_json_file('./result/', user_fbid + '_' + 'get_check_in_with_time', data)

            print(data)

            # 把資料寫入到資料庫
            # fb_crawler.set_check_in_with_time(user_fbid,data)

            i+=1
            if i % 20 == 0:
                print('第{0}筆'.format(i))

    # 針對chrome版本設計,請使用browser.prepare_chrome
    # PS:不需要scroll!
    def get_fbpage_informaton(self, fbids):
        browser = Browser()
        browser.prepare_chrome(None)
        browser.login_fb()

        page_source = ''

        i = 0
        for fbpage_id in fbids:
            url_obj = Url_manager()
            url_obj.use_mobile_version()
            url = url_obj.get_fbpage_informaton_url(fbpage_id)

            if  browser.is_exist_in_cache(url):
                print("從快取中讀取 : {0}".format(re.sub(r'[^a-z0-9]', '', url) + '.html'))
                page_source = browser.read_cache(url)
            else :
                print("爬取: {0}".format(url))
                browser.nav(url)
                page_source = browser.save()

            data = fb_crawler.get_fbpage_informaton(page_source)
            write_json_file('./result/', fbpage_id + '_' + 'get_fbpage_informaton', data)


            i += 1
            if i % 20 == 0:
                print('第{0}筆'.format(i))

def read_from_json_file(path):
    '''從目錄讀取下讀取包含使用者fbid的JSON檔
    Args:
        path: 檔案路徑
    Returns:
        fbids : 包含使用者Fbid的list
    '''

    f = open(path, 'r')
    fbids = json.load(f)['fbids']
    return fbids

def write_json_file(path,file_name,data):
    fo = open(path+file_name+'.json', 'w')
    fo.write(demjson.encode(data))



def main():
    argv = ''
    if (len(sys.argv) > 1):
        argv = sys.argv[1]

    if argv == 'get_personal_information':
        fbids = read_from_json_file('user_fbid_example.json')
        task = Task()
        task.get_personal_information(fbids)
    elif argv == 'get_fbuser_like_fbpage':
        fbids = read_from_json_file('user_fbid_example.json')
        task = Task()
        task.get_fbuser_like_fbpage(fbids)
    elif argv == 'get_check_in_with_time':
        fbids = read_from_json_file('user_fbid_example.json')
        task = Task()
        task.get_check_in_with_time(fbids)

    elif argv == 'get_fbpage_informaton':
        fbids = read_from_json_file('fbpage_fbid_example.json')
        task = Task()
        task.get_fbpage_informaton(fbids)




if __name__ == '__main__':
    main()
