# coding=utf-8
from datetime import datetime, date
import yaml
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from TXAPI import TXAPI

class GFEverydayEmail:
    # 注意：顺序影响短信编辑
    zaoan_apis = ["zaoan", "theone", "tianqi"]
    wanan_apis = ["qinghua", "wanan"]

    def __init__(self):
        self.email_list, self.dictum_channels, self.text_emoji_file, tx_api_key, self.email_smtp_pwd = self.get_init_data()
        self.tx_api = TXAPI(tx_api_key)

    def get_init_data(self):
        '''
        初始化基础数据
        :return: None
        '''
        with open('_config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.Loader)
        morning_alarm_timed = config.get('morning_alarm_timed').strip()
        evening_alarm_timed = config.get('evening_alarm_timed').strip()
        init_msg = f"每天定时发送时间：早-{morning_alarm_timed}, 晚-{evening_alarm_timed}\n"

        morning_dictum_channel = config.get('morning_dictum_channel', '')
        evening_dictum_channel = config.get('evening_dictum_channel', '')
        dictum_channels = [morning_dictum_channel, evening_dictum_channel]
        init_msg += f"信息获取渠道：早-{morning_dictum_channel}, 晚-{evening_dictum_channel}\n\n"

        text_emoji_file = config.get('text_emoji_file', '')
        init_msg += f"text_emoji文件名：{text_emoji_file}\n"

        email_list = []
        email_infos = config.get('email_infos')
        for email_info in email_infos:
            email = {}
            email_file = email_info.get('email_file').strip()
            email["email_list"] = []
            with open(email_file, "r") as file:
                lines = file.readlines()
            for line in lines:
                email_path = line.strip()
                if len(email_path)>0:
                    email["email_list"].append(email_path)
            email["gf_name"] = email_info.get('gf_name', '')
            email["city_name"] = email_info.get('city_name', '')
            email["start_date"] = email_info.get('start_date', '')
            email["sweet_words"] = email_info.get('sweet_words', '')

            email_list.append(email)
            print_msg = f"邮箱地址：{str(email['email_list'])}\n" \
                        f"女友所在地区：{email['city_name']}\n" \
                        f"在一起的第一天日期：{email['start_date']}\n" \
                        f"最后一句为：{email['sweet_words']}\n\n"
            init_msg += print_msg

        tx_api_key = ''
        email_smtp_pwd = ''
        try:
            with open(config.get('tx_api_key_file', 'no_config'), "r") as file:
                tx_api_key = file.readline().strip()
            with open(config.get('email_smtp_pwd_file', 'no_config'), "r") as file:
                email_smtp_pwd = file.readline().strip()
        except:
            print("获取 API Key 失败，文件打开失败！请检查是否存在配置文件中的 api_key_file...\n")

        init_msg += f"tx_api_key:{tx_api_key}\nemail_smtp_pwd:{email_smtp_pwd}\n"

        print(u"*" * 25 + "init msg" + u"*" * 25)
        print(init_msg)

        return email_list, dictum_channels, text_emoji_file, tx_api_key, email_smtp_pwd

    def start_today_info(self, chat_id, send_test=False):
        '''
        每日定时开始处理。
        :param chat_id:int, 判断早晚安信息（0：早安，1：晚安）。
        :param send_test:bool, 测试标志，当为True时，不发送信息。
        :return: None。
        '''
        print("*" * 20 + "start_today_info" + "*" * 20)
        print("chat_id:", chat_id, "send_test:", send_test)
        print("获取相关信息...")
        date_str = date.today().strftime('%Y-%m-%d')
        for email in self.email_list:
            days = (datetime.strptime(date_str, '%Y-%m-%d') - datetime.strptime(email["start_date"], '%Y-%m-%d')).days
            # 判断早安还是晚安
            if chat_id == 0:
                email_msg = f"{email['gf_name']}，今天是我们相恋的第{days}天！想你~\n"
                email_title = "迪迪早安~"
                apis = self.zaoan_apis
            elif(chat_id == 1):
                email_msg = f"{email['gf_name']}，我们相恋的第{days}天就要结束啦！爱你~\n"
                email_title = "迪迪晚安~"
                apis = self.wanan_apis
            else:
                print("Wrong chat id!!!")
                return
            # 构建短信
            for k in apis:
                email_msg += self.tx_api.get_channel_msg(k, date_str, email["city_name"])
            email_msg += email['sweet_words']
            email_msg += self.get_text_emoji()
            # 发送短信
            if len(email["email_list"]) <= 0:
                print("No Phone Number with msg:", email_msg)
                return
            else:
                if not send_test:
                    for receiver in email["email_list"][1:]:
                        self.send_email(email["email_list"][0], receiver, email_title, email_msg)
                else:
                    print(f"发送给{email['email_list'][1:]}成功:\n", email_msg)
                return

    def get_text_emoji(self):
        '''
        随机获取一个 text emoji 作为结束标记
        :return: str text_emoji
        '''
        text_emoji = []
        with open(self.text_emoji_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        for line in lines:
            if len(line) > 0:
                text_emoji.append(line)
        return random.choice(text_emoji)
        
    def send_email(self, sender, receiver, email_title, email_msg):
        print("*" * 10 + "sending email" + "*" * 10)

        message = MIMEText(email_msg, 'plain', 'utf-8')
        message['From'] = Header('小田助手', 'utf-8')
        message['To'] = Header('最爱的迪迪', 'utf-8')
        message['Subject'] = Header(email_title, 'utf-8')
        try:
            ### 使用 SMTP 发送
            # server = smtplib.SMTP('smtp.exmail.qq.com')
            # server.login(sender, self.email_smtp_pwd)
            # server.sendmail(sender, receiver, message.as_string())
            # server.quit()

            ### 使用 SMTP_SSL 发送
            server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
            server.login(sender, self.email_smtp_pwd)
            server.sendmail(sender, receiver, message.as_string())
            server.close()
            print(f"发送给{receiver}成功:\n", email_msg)
        except smtplib.SMTPException as e:
            print("Failed to sent email:\n" + str(e))
            print(message.as_string())
            print(email_msg)


if __name__ == '__main__':
    g = GFEverydayEmail()
    g.start_today_info(0, send_test=True)
    g.start_today_info(1, send_test=True)