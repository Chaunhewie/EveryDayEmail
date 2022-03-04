import os
import time
import json
import requests
from datetime import datetime, date, timedelta


class TXAPI:
    weather_icons = {"风": 1, "云": 2, "雨": 3, "雪": 4, "霜": 5, "露": 6, "雾": 7, "雷": 8, "晴": 9, "阴": 10,
                     "feng": 1, "yun": 2, "yu": 3, "xue": 4, "shuang": 5, "lu": 6, "wu": 7, "lei": 8, "qing": 9, "yin": 10}
    urls = {"zaoan": 'http://api.tianapi.com/txapi/zaoan/index?key={0}',
            "tianqi": 'http://api.tianapi.com/txapi/tianqi/index?key={0}&city={1}',
            "aqi": 'http://api.tianapi.com/txapi/aqi/index?key={0}&area={1}',
            "wanan": 'http://api.tianapi.com/txapi/wanan/index?key={0}',
            "qinghua": 'http://api.tianapi.com/txapi/saylove/index?key={0}',
            "theone": 'http://api.tianapi.com/txapi/one/index?key={0}&date={1}'}
    cache_dir = "./cache/"
    weather_icons_dir = "./resources/weather"  # (.resources/weather | .resources/weather-black)
    weather_icons_mapping_file = "./resources/weather_names.json"  # 天气名字和天气icon的对应关系
    weather_icons_git_path = "https://github.com/Chaunhewie/EveryDayEmail/tree/master/resources/weather"

    def __init__(self, tx_api_key, date_str):
        self.tx_api_key = tx_api_key
        self.date_str = date_str
        self.content = {}
        self.city_name = ""

        with open(self.weather_icons_mapping_file, "r", encoding="utf-8") as f:
            self.weather_icons = json.load(f)

        # make cache dirs
        for f in self.urls.keys():
            if not os.path.exists(os.path.join(self.cache_dir, f)):
                os.mkdir(os.path.join(self.cache_dir, f))

    def channel_msg(self, channel, city_name):
        """
        获取天行数据上面的channel信息
        :param channel: 支持的 channel 见 self.urls.keys()
        :param city_name: 用于获取该城市天气数据
        :return: 组合好的 html 数据
        """
        self.city_name = city_name
        urls, cache_folders = getattr(self, channel + "_urls")()
        content = {}
        for i, (url, cache_folder) in enumerate(zip(urls, cache_folders)):
            c = self.scrapy_url(url, file_path=os.path.join(self.cache_dir, cache_folder, self.date_str + ".txt"))
            c = c.get('newslist', [{}])[0]
            for k, v in c.items():
                if k not in content:
                    content[k] = v
        self.content = content
        return getattr(self, channel + "_msg")()

    def theone_img(self):
        """
        获取 theone 的每日图片
        :return: 图片的 src 链接
        """
        print("*" * 10 + "getting the one img" + "*" * 10)
        url = self.urls["theone"].format(self.tx_api_key, self.date_str)
        content = self.scrapy_url(url, os.path.join(self.cache_dir, "theone", self.date_str + ".txt"))
        return content['newslist'][0]["imgurl"]

    def scrapy_url(self, url, file_path=""):
        '''
        爬取url数据
        :param url: 请求地址
        :param file_name: 缓存文件名
        :return: url爬取的内容数据
        '''
        print("*" * 10 + "getting url info" + "*" * 10)
        if (os.path.exists(file_path)):
            print("reading cache file: ", file_path)
            with open(file_path, "r", encoding="utf-8") as file:
                content = json.load(file)
        else:
            while True:
                print("request url: ", url)
                resp = requests.get(url)
                content = json.loads(resp.text)
                if content:
                    print(content)
                if content['code'] == 200:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(json.dumps(content))
                    break
                else:
                    print("req error, sleep 1 second and retry...")
                    time.sleep(1)
        return content

    def tianqi_urls(self):
        return [self.urls["tianqi"].format(self.tx_api_key, self.city_name),
                self.urls["aqi"].format(self.tx_api_key, self.city_name)], ["tianqi", "aqi"]

    def zaoan_urls(self):
        return [self.urls["zaoan"].format(self.tx_api_key)], ["zaoan"]

    def wanan_urls(self):
        return [self.urls["wanan"].format(self.tx_api_key)], ["wanan"]

    def qinghua_urls(self):
        return [self.urls["qinghua"].format(self.tx_api_key)], ["qinghua"]

    def theone_urls(self):
        days_before = datetime.today() + timedelta(-3)
        the_one_date_str = days_before.strftime('%Y-%m-%d')
        return [self.urls["theone"].format(self.tx_api_key, the_one_date_str)], ["theone"]

    def tianqi_msg(self):
        c = self.content
        date_str = self.date_str
        return f"<p>***天气预报来袭~~~<br>" \
               f"***{c.get('date', date_str)} {c.get('week', '')}<br>" \
               f"***今日{c.get('weather', '-')}<br>" \
               f"***气温{c.get('lowest', '-℃')}/{c.get('highest', '-℃')}，当前气温{c.get('real', '-℃')}<br>" \
               f"***风速: {c.get('windspeed', '-')}({c.get('windsc', '-')})<br>" \
               f"***PM2.5: {c.get('pm2_5', '-')}({c.get('quality', '-')})</p>\n"

    def zaoan_msg(self):
        c = self.content
        if "早安" in c.get("content", ''):
            return "<p>" + c.get("content", '') + "</p>\n"
        return "<p>早安~<br>" + c.get("content", '') + "</p>\n"

    def wanan_msg(self):
        c = self.content
        if "晚安" in c.get("content", ''):
            return "<p>" + c.get("content", '') + "</p>\n"
        return "<p>" + c.get("content", '') + "<br>晚安~</p>\n"

    def qinghua_msg(self):
        c = self.content
        return "<p>" + c.get("content", '') + "</p>\n"

    def theone_msg(self):
        c = self.content
        return "<p>" + c.get("word", '') + "</p>\n"

    def test_show_tianqi(self):
        """获取已经爬取的天气名称，用于对齐 .resources/weather_names.json"""
        files = os.listdir(os.path.join(self.cache_dir, "tianqi"))
        tianqi = set()
        for fname in files:
            with open(os.path.join(self.cache_dir, "tianqi", fname), "r", encoding="utf-8") as f:
                d = json.load(f)
            if "转" in d["newslist"][0]["weather"]:
                w = d["newslist"][0]["weather"].split("转")
            else:
                msg = "<p>" + c.get("content", '') + "<br>晚安~</p>\n"
        elif channel == "qinghua":
            msg = "<p>" + c.get("content", '') + "</p>\n"
        elif channel == "theone":
            msg = "<p>" + c.get("word", '') + "</p>\n"
        else:
            msg = "<p>" + c.get("content", '') + "</p>\n"
        return msg

    def test_show_tianqi(self):
        files = os.listdir(os.path.join(self.cache_dir, "tianqi"))
        tianqi = set()
        for fname in files:
            with open(os.path.join(self.cache_dir, "tianqi", fname), "r") as f:
                d = json.load(f)
            if "转" in d["newslist"][0]["weather"]:
                w = d["newslist"][0]["weather"].split("转")
            else:
                w = [d["newslist"][0]["weather"]]
            for i in w:
                tianqi.add(i)
        print(tianqi)

# {'中雨转小雨', '小雨', '晴转小雨', '多云', '多云转晴', '中雨转多云', '暴雨转大雨', '晴', '晴转多云', '中雨', '阵雨转大雨', '小雨转多云', '阴转晴', '阴'
# , '中雨转阵雨', '小雨转阴', '多云转小雨', '阴转小雨', '小雨转大雨'}

if __name__ == "__main__":
    tx = TXAPI("")
    tx.test_show_tianqi()
