import json
import time
import urllib.request
import urllib.parse
from core import info_collection
from conf import settings

class ArgvHandler(object):
    def __init__(self, args):
        self.args = args
        self.parse_args()

    def parse_args(self):
        if len(self.args) > 1 and hasattr(self, self.args[1]):
            func = getattr(self, self.args[1])
            func()
        else:
            self.help_msg()

    def help_msg(self):
        """
                帮助说明
                :return:
                """
        msg = '''
                参数名               功能

                collect_data        测试收集硬件信息的功能

                report_data         收集硬件信息并汇报
                '''
        print(msg)

    @staticmethod
    def collet_data():
        info = info_collection.InfoCollection()
        asset_data = info.collect()
        print(asset_data)

    @staticmethod
    def report_data():
        info = info_collection.InfoCollection()
        asset_data = info.collect()
        data = {'asset_data': json.dumps(asset_data)}
        url = 'http://%s:%s%s' % (settings.Params['server'], settings.Params['port'], settings.Params['url'])
        print('正在将数据发送至 [%s]......' % url)
        try:
            data_encode = urllib.parse.urlencode(data).encode()
            response = urllib.request.urlopen(url=url, data=data_encode, timeout=settings.Params['request_timeout'])
            print("\033[31;1m发送完毕！\033[0m ")
            message = response.read().decode()
            print('返回结果：%s' % message)
        except Exception as e:
            message = '发送失败' + '错误原因： {}'.format(e)
            print("\033[31;1m发送失败，错误原因： %s\033[0m" % e)

        with open(settings.PATH, 'ab') as f:
            log = '发送时间：%s \t 服务器地址：%s \t 返回结果：%s \n' % (time.strftime('%Y-%m-%d %H:%M:%S'), url, message)
            f.write(log.encode())
            print('日志记录成功！！！')

