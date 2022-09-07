import requests
from random import randint
import xlrd
import json


class My_request(object):

    # 对返回值进行处理
    def __str__(self):

        # return "%r"%self.connect()
        return str("%r"%self.connect())

    # 获取表格数据
    def connect(self):

        excelDir = 'D:\test.xls'

        # 打开Excel文件 formatting_info=True :保持原样式
        self.workBook = xlrd.open_workbook(excelDir, formatting_info=True)

        # 获取所有表名
        sheets = self.workBook.sheet_names()

        # 需要执行的sheet
        workSheet = self.workBook.sheet_by_name('测试用例2')

        # 获取一行
        # cellData = workSheet.row_values(1)

        # 获取单元格 获取的不是字符串 而是excel 格式参数
        cellData = workSheet.cell(1, 0)

        return cellData.value

    # token函数 调用函数就可获取token值 再用到新增接口
    def get_token(self):
        # 获取token
        token_urls = 'http://47.96.181.17:9090/rest/toController'
        payload = {'userName': 'J201903070064', 'password': '362387359'}

        # 发送请求 json 请求体
        res = requests.post(token_urls, json=payload)
        return res.json()['token']

    #  新增用户接口
    def add_user(self, bodyData):
        """
        :param bodyData: request body
        :return:  res data
        """

        self.addUsr_url = 'http://47.96.181.17:9090/rest/ac01CrmController'

        # 对字符串转换字典 json 串
        self.payload = json.loads(bodyData)

        # 对手机号进行参数化
        self.payload['aac030'] = f'134{randint(11111111,99999999)}'

        self.header_addusr = {'Content-Type': 'application/json', 'X-AUTH-TOKEN': self.get_token()}

        # # 发送请求 url 请求体
        res = requests.post(self.addUsr_url, json=self.payload, headers = self.header_addusr)

        self.rest = res.json()
        # 打印输出结果 是否注册成功
        print(res.json())

        return res.json()

    def write_index(self, datas):
        from xlutils.copy import copy
        # 对表复制 原始的测试用例不会改变
        newWoekBook = copy(self.workBook)

        # 取拷贝的excel的sheet 下标
        newSheet = newWoekBook.get_sheet(1)

        # 写入数据 第一行第一列
        newSheet.write(1, 1, datas)

        # 保存新生成的 excel对象
        newWoekBook.save('../data/res.xls')

    def write_in(self):

        # 如果已经有数据了 就需要对原表进行复制

        if self.rest['message'] == '成功':
            info = 'pass'

            self.write_index(info)

        else:
            info = 'fail'
            self.write_index(info)


if __name__ == '__main__':

    re = My_request()
    re.add_user(re.connect())

    re.write_in()