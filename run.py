# coding=utf-8
import sys
from GFEverydayEmail import GFEverydayEmail


def run(chat_id):
    '''
    主程序入口
    :return:
    '''
    GFEverydayEmail().start_today_info(chat_id)


def test_run(chat_id):
    '''
    运行前的测试
    :return:
    '''
    GFEverydayEmail().start_today_info(chat_id, send_test=True)

if __name__ == '__main__':
    print("参数列表：", str(sys.argv))
    chat_id = 0
    try:
        chat_id = int(sys.argv[1])
    except:
        print("char_id should be integer such as 0 or 1")
    run(chat_id)
