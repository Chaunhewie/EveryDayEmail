import os
import time
import json
import requests


class TXAPI:
    weather_types = {"风": 1, "云": 2, "雨": 3, "雪": 4, "霜": 5, "露": 6, "雾": 7, "雷": 8, "晴": 9, "阴": 10,
                     "feng": 1, "yun": 2, "yu": 3, "xue": 4, "shuang": 5, "lu": 6, "wu": 7, "lei": 8, "qing": 9, "yin": 10}
    urls = {"zaoan": 'http://api.tianapi.com/txapi/zaoan/index?key={0}',
            "tianqi": 'http://api.tianapi.com/txapi/tianqi/index?key={0}&city={1}',
            "wanan": 'http://api.tianapi.com/txapi/wanan/index?key={0}',
            "qinghua": 'http://api.tianapi.com/txapi/saylove/index?key={0}',
            "theone": 'http://api.tianapi.com/txapi/one/index?key={0}&date={1}'}

    def __init__(self, tx_api_key):
        self.tx_api_key = tx_api_key

    def get_channel_msg(self, channel, date_str, city_name):
        if channel == "tianqi":
            url = self.urls[channel].format(self.tx_api_key, city_name)
        elif channel == "theone":
            url = self.urls[channel].format(self.tx_api_key, date_str)
        else:
            url = self.urls[channel].format(self.tx_api_key)
        content = self.get_url_info(url, "./cache/" + channel + "/" + date_str + ".txt")
        # return self.execute_contents(channel, content)
        return self.execute_contents_for_html(channel, content)

    def get_the_one_img(self, date_str, channel="theone"):
        print("*" * 10 + "getting the one img" + "*" * 10)
        url = self.urls[channel].format(self.tx_api_key, date_str)
        content = self.get_url_info(url, "./cache/" + channel + "/" + date_str + ".txt")
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

    def execute_contents(self, channel, content):
        '''
        处理从api得到的content，并返回所需要的txt格式的msg
        :param channel: 请求类型
        :param content: url返回内容
        :return: url返回内容的处理结果
        '''
        c = content['newslist'][0]
        if channel == "tianqi":
            msg = f"***天气预报来袭~~~\n" \
                  f"***{c['date']} {c['week']}\n" \
                  f"***今日{c['weather']}\n" \
                  f"***气温{c['lowest']}/{c['highest']}，当前气温{c['real']}\n" \
                  f"***风力{c['windspeed']}\n" \
                  f"***空气质量 {c['air_level']}\n"
        elif channel == "zaoan":
            if "早安" in c["content"]:
                msg = c["content"] + "\n"
            else:
                msg = "早安~\n" + c["content"] + "\n"
        elif channel == "wanan":
            if "晚安" in c["content"]:
                msg = c["content"] + "\n"
            else:
                msg = c["content"] + "\n晚安~\n"
        elif channel == "qinghua":
            msg = c["content"] + "\n"
        elif channel == "theone":
            msg = c["word"] + "\n"
        else:
            msg = c["content"] + "\n"
        return msg

    def execute_contents_for_html(self, channel, content):
        '''
        处理从api得到的content，并返回所需要的html格式的msg
        :param channel: 请求类型
        :param content: url返回内容
        :return: url返回内容的处理结果
        '''
        c = content['newslist'][0]
        if channel == "tianqi":
            msg = f"<p>***天气预报来袭~~~<br>" \
                  f"***{c['date']} {c['week']}<br>" \
                  f"***今日{c['weather']}\n" \
                  f"***气温{c['lowest']}/{c['highest']}，当前气温{c['real']}<br>" \
                  f"***风力{c['windspeed']}<br>" \
                  f"***空气质量 {c['air_level']}</p>\n"
        elif channel == "zaoan":
            if "早安" in c["content"]:
                msg = "<p>" + c["content"] + "</p>\n"
            else:
                msg = "<p>早安~<br>" + c["content"] + "</p>\n"
        elif channel == "wanan":
            if "晚安" in c["content"]:
                msg = "<p>" + c["content"] + "</p>\n"
            else:
                msg = "<p>" + c["content"] + "<br>晚安~</p>\n"
        elif channel == "qinghua":
            msg = "<p>" + c["content"] + "</p>\n"
        elif channel == "theone":
            msg = "<p>" + c["word"] + "</p>\n"
        else:
            msg = "<p>" + c["content"] + "</p>\n"
        return msg