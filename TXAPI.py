import os
import time
import json
import requests
from datetime import datetime, date, timedelta

class TXAPI:
    weather_types = {"风": 1, "云": 2, "雨": 3, "雪": 4, "霜": 5, "露": 6, "雾": 7, "雷": 8, "晴": 9, "阴": 10,
                     "feng": 1, "yun": 2, "yu": 3, "xue": 4, "shuang": 5, "lu": 6, "wu": 7, "lei": 8, "qing": 9, "yin": 10}
    urls = {"zaoan": 'http://api.tianapi.com/txapi/zaoan/index?key={0}',
            "tianqi": 'http://api.tianapi.com/txapi/tianqi/index?key={0}&city={1}',
            "aqi": 'http://api.tianapi.com/txapi/aqi/index?key={0}&area={1}',
            "wanan": 'http://api.tianapi.com/txapi/wanan/index?key={0}',
            "qinghua": 'http://api.tianapi.com/txapi/saylove/index?key={0}',
            "theone": 'http://api.tianapi.com/txapi/one/index?key={0}&date={1}'}
    cache_dir = "./cache/"

    def __init__(self, tx_api_key):
        self.tx_api_key = tx_api_key

        # make cache dirs
        for f in self.urls.keys():
            if not os.path.exists(os.path.join(self.cache_dir, f)):
                os.mkdir(os.path.join(self.cache_dir, f))

    def get_channel_msg(self, channel, date_str, city_name):
        urls = []
        cache_folders = []
        if channel == "tianqi":
            urls.append(self.urls[channel].format(self.tx_api_key, city_name))  # 天气API
            cache_folders.append(channel)
            urls.append(self.urls["aqi"].format(self.tx_api_key, city_name))  # 空气质量API
            cache_folders.append("aqi")
        elif channel == "theone":
            days_before = datetime.today() + timedelta(-3)
            the_one_date_str = days_before.strftime('%Y-%m-%d')
            urls.append(self.urls[channel].format(self.tx_api_key, the_one_date_str))
            cache_folders.append(channel)
        else:
            urls.append(self.urls[channel].format(self.tx_api_key))
            cache_folders.append(channel)
        content = {}
        for i, url in enumerate(urls):
            c = self.get_url_info(url, os.path.join(self.cache_dir, cache_folders[i], date_str + ".txt"))
            c = c.get('newslist', [{}])[0]
            for k, v in c.items():
                if k not in content:
                    content[k] = v
        # return self.execute_contents(channel, content)
        return self.execute_contents_for_html(channel, content, date_str)

    def get_the_one_img(self, date_str, channel="theone"):
        print("*" * 10 + "getting the one img" + "*" * 10)
        url = self.urls[channel].format(self.tx_api_key, date_str)
        content = self.get_url_info(url, os.path.join(self.cache_dir, channel, date_str + ".txt"))
        return content['newslist'][0]["imgurl"]

    def get_url_info(self, url, file_path=""):
        '''
        获取url的返回值
        :param url: 请求地址
        :param file_name: 缓存文件名
        :return: url返回内容的处理结果
        '''
        print("*" * 10 + "getting url info" + "*" * 10)
        if(os.path.exists(file_path)):
            print("reading cache file: ", file_path)
            with open(file_path, "r") as file:
                content = json.load(file)
        else:
            while True:
                print("request url: ", url)
                resp = requests.get(url)
                content = json.loads(resp.text)
                if content:
                    print(content)
                if content['code'] == 200:
                    with open(file_path, "w") as file:
                        file.write(json.dumps(content))
                    break
                else:
                    print("req error, sleep 1 second and retry...")
                    time.sleep(1)
        return content

    def execute_contents(self, channel, content, date_str=""):
        '''
        处理从api得到的content，并返回所需要的txt格式的msg
        :param channel: 请求类型
        :param content: url返回内容
        :return: url返回内容的处理结果
        '''
        c = content
        if channel == "tianqi":
            msg = f"***天气预报来袭~~~\n" \
                  f"***{c.get('date', date_str)} {c.get('week', '')}\n" \
                  f"***今日{c.get('weather', '-')}\n" \
                  f"***气温{c.get('lowest', '-℃')}/{c.get('highest', '-℃')}，当前气温{c.get('real', '-℃')}\n" \
                  f"***风速{c.get('windspeed', '-')}({c.get('windsc', '-')})\n" \
                  f"***PM2.5 {c.get('pm2_5', '-')}({c.get('quality', '-')})\n"
        elif channel == "zaoan":
            if "早安" in c.get("content", ''):
                msg = c.get("content", '') + "\n"
            else:
                msg = "早安~\n" + c.get("content", '') + "\n"
        elif channel == "wanan":
            if "晚安" in c.get("content", ''):
                msg = c.get("content", '') + "\n"
            else:
                msg = c.get("content", '') + "\n晚安~\n"
        elif channel == "qinghua":
            msg = c.get("content", '') + "\n"
        elif channel == "theone":
            msg = c.get("word", '') + "\n"
        else:
            msg = c.get("content", '') + "\n"
        return msg

    def execute_contents_for_html(self, channel, content, date_str=''):
        '''
        处理从api得到的content，并返回所需要的html格式的msg
        :param channel: 请求类型
        :param content: url返回内容
        :return: url返回内容的处理结果
        '''
        c = content
        if channel == "tianqi":
            msg = f"<p>***天气预报来袭~~~<br>" \
                  f"***{c.get('date', date_str)} {c.get('week', '')}<br>" \
                  f"***今日{c.get('weather', '-')}<br>" \
                  f"***气温{c.get('lowest', '-℃')}/{c.get('highest', '-℃')}，当前气温{c.get('real', '-℃')}<br>" \
                  f"***风速: {c.get('windspeed', '-')}({c.get('windsc', '-')})<br>" \
                  f"***PM2.5: {c.get('pm2_5', '-')}({c.get('quality', '-')})</p>\n"
        elif channel == "zaoan":
            if "早安" in c.get("content", ''):
                msg = "<p>" + c.get("content", '') + "</p>\n"
            else:
                msg = "<p>早安~<br>" + c.get("content", '') + "</p>\n"
        elif channel == "wanan":
            if "晚安" in c.get("content", ''):
                msg = "<p>" + c.get("content", '')+ "</p>\n"
            else:
                msg = "<p>" + c.get("content", '') + "<br>晚安~</p>\n"
        elif channel == "qinghua":
            msg = "<p>" + c.get("content", '') + "</p>\n"
        elif channel == "theone":
            msg = "<p>" + c.get("word", '') + "</p>\n"
        else:
            msg = "<p>" + c.get("content", '') + "</p>\n"
        return msg