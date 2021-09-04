import requests
import json
import time
import datetime
import random
from lxml import etree


class QUSTClassChooser:
    config = {}

    interval = 1
    page_interval = 0.3

    su = ''
    headers = {}
    base_url = ''

    if_rand = 0
    randl = 1
    randr = 5

    xkkz_id = ''
    kcgs_dict = {}

    def __init__(self) -> None:
        with open('config.json', 'r', encoding='utf8') as f:
            self.config = json.loads(f.read())
        self.interval = self.config['interval'] / 1000.0
        self.page_interval = self.config['page_interval'] / 1000.0
        self.su = self.config['su']
        self.headers = {
            "Cookie": self.config['cookie'],
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/93.0.4577.63 Safari/537.36 "
        }
        self.base_url = self.config['base_url']
        self.if_rand = self.config['if_rand']
        if self.if_rand == 1:
            self.randl = self.config['randl'] / 1000.0
            self.randr = self.config['randr'] / 1000.0
        self.xkkz_id = self.get_xkkz_id()
        self.kcgs_dict = self.get_kcgs_id()

    def get_kcgs_id(self):
        r = requests.post(
            url=self.base_url + '/jwglxt/xkgl/common_queryKcgsPaged.html?gnmkdm=N253512&su=' + self.su,
            headers=self.headers,
            data={
                'queryModel.currentPage': 1,
                'queryModel.showCount': 100,
                'minNum': 7,
                'maxNum': 100,
                'queryModel.sortOrder': 'asc',
                'queryModel.sortName': 'kcgsdm',
                'rangeable': 'true'
            }
        )
        result = {}
        tmp = json.loads(r.text)['items']
        for i in tmp:
            result[i['kcgsmc']] = i['kcgsdm']
        return result

    def get_xkkz_id(self) -> str:
        r = requests.get(
            url=self.base_url + '/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su=' + self.su,
            headers=self.headers
        )
        return etree.HTML(r.text).xpath('//*[@id="nav_tab"]/li[2]/a/@onclick')[0].split(',')[2].strip('\'')

    def get_class_list(self, page) -> list:
        r = requests.post(
            url=self.base_url + '/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=' + self.su,
            headers=self.headers,
            data=self.make_get_class_list_data(page)
        )
        return json.loads(r.text)['tmpList']

    def get_class_detail(self, item) -> dict:
        r = requests.post(
            url=self.base_url + '/jwglxt/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su=' + self.su,
            headers=self.headers,
            data=self.make_get_class_detail_data(item)
        )
        return json.loads(r.text)[0]

    def choose_class(self, data1, data2):
        r = requests.post(
            url=self.base_url + '/jwglxt/xsxk/zzxkyzbjk_xkBcZyZzxkYzb.html?gnmkdm=N253512&su=' + self.su,
            headers=self.headers,
            data=self.make_choose_class_data(data1, data2)
        )
        return json.loads(r.text)

    def make_get_class_list_data(self, cnt: int) -> dict:
        dat = {'rwlx': self.config['rwlx'], 'xkly': self.config['xkly'], 'bklx_id': self.config['bklx_id'],
               'sfkkjyxdxnxq': self.config['sfkkjyxdxnxq'], 'xqh_id': self.config['xqh_id'], 'jg_id': self.su[2:4],
               'njdm_id_1': '20' + self.su[0:2], 'zyh_id_1': self.su[2:6], 'zyh_id': self.su[2:6],
               'zyfx_id': self.config['zyfx_id'], 'njdm_id': '20' + self.su[0:2], 'bh_id': self.su[0:8],
               'xbm': self.config['xbm'], 'xslbdm': self.config['xslbdm'], 'ccdm': self.config['ccdm'],
               'xsbj': self.config['xsbj'], 'sfkknj': self.config['sfkknj'], 'sfkkzy': self.config['sfkkzy'],
               'kzybkxy': self.config['kzybkxy'], 'sfznkx': self.config['sfznkx'], 'zdkxms': self.config['zdkxms'],
               'sfkxq': self.config['sfkxq'], 'sfkcfx': self.config['sfkcfx'], 'kkbk': self.config['kkbk'],
               'kkbkdj': self.config['kkbkdj'], 'sfkgbcx': self.config['sfkgbcx'],
               'sfrxtgkcxd': self.config['sfrxtgkcxd'], 'tykczgxdcs': self.config['tykczgxdcs'],
               'xkxnm': datetime.datetime.now().year, 'xkxqm': self.config['xkxqm'], 'kklxdm': self.config['kklxdm'],
               'rlkz': self.config['rlkz'], 'xkzgbj': self.config['xkzgbj'], 'kspage': 1 + cnt * 10,
               'jspage': (cnt + 1) * 10, 'jxbzb': self.config['jxbzb']}
        for index, value in enumerate(self.config['filter']):
            dat['filter_list[' + str(index) + ']'] = value
        for index, value in enumerate(self.config['kcgs']):
            dat['kcgs_list[' + str(index) + ']'] = self.kcgs_dict[value]
        if self.config['yl'] == 1:
            dat['yl_list[0]'] = 1
        return dat

    def make_get_class_detail_data(self, item) -> dict:
        dat = self.make_get_class_list_data(0)
        del dat['xkzgbj']
        del dat['kspage']
        del dat['jspage']
        del dat['jxbzb']
        dat['kch_id'] = item['kch_id']
        dat['xkkz_id'] = self.xkkz_id
        dat['cxbj'] = self.config['cxbj']
        dat['fxbj'] = self.config['fxbj']
        return dat

    def make_choose_class_data(self, data1, data2) -> dict:
        dat = {'jxb_ids': data2['do_jxb_id'], 'kch_id': data1['kch_id'], 'rwlx': self.config['rwlx'],
               'rlkz': self.config['rlkz'], 'rlzlkz': self.config['rlzlkz'], 'sxbj': self.config['sxbj'],
               'xxkbj': self.config['xxkbj'], 'qz': self.config['qz'], 'cxbj': self.config['cxbj'],
               'xkkz_id': self.xkkz_id, 'njdm_id': '20' + self.su[0:2], 'zyh_id': self.su[2:6],
               'kklxdm': self.config['kklxdm'], 'xklc': self.config['xklc'], 'xkxnm': datetime.datetime.now().year,
               'xkxqm': self.config['xkxqm']}
        return dat

    def get_interval(self):
        if self.if_rand == 1:
            return random.uniform(self.randl, self.randr)
        else:
            return self.interval

    def run(self):
        cnt = 0
        while True:
            cnt = cnt + 1
            page = 0
            print('\r', '已刷新' + str(cnt) + '次', end='')
            while True:
                lis = self.get_class_list(page)
                for i in lis:
                    detail = self.get_class_detail(i)
                    result = self.choose_class(i, detail)
                    if result['flag'] == '1':
                        print('\n [成功]  ' + i['kcmc'])
                        exit(0)
                    else:
                        print('\r', '[失败]  ' + i['kcmc'] + ' ' + str(result))
                time.sleep(self.page_interval)
                page = page + 1
                if len(lis) != 10:
                    break
            time.sleep(self.get_interval())


if __name__ == "__main__":
    ins = QUSTClassChooser()
    ins.run()
