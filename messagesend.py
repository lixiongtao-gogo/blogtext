'''
author = 李雄涛
data = 2020/3/6
当前py文件的作用：
'''
import random
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

ACCESS_KEY_ID = ""  #用户AccessKey  需要根据自己的账户修改
ACCESS_KEY_SECRET = ""  #Access Key Secret  需要根据自己的账户修改

class SMS:
    def __init__(self,signName,templateCode):
        self.signName = signName  #签名
        self.templateCode = templateCode  #模板code
        self.client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, 'cn-hangzhou')

    def send(self,phone_numbers,template_param):
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone_numbers)
        request.add_query_param('SignName', self.signName)
        request.add_query_param('TemplateCode', self.templateCode)
        request.add_query_param('TemplateParam', template_param)
        response = self.client.do_action_with_exception(request)
        return response

#实例话一个短信对象
sms = SMS("学习验证码", "SMS_184826920")

    # num = random.randint(1000,9999)
    # #使用session签字，用于之后验证输入的和收到是否一直
    # session['sms'] = str(num)
    # para = "{'number':'%d'}"%num
    # sms.send()

