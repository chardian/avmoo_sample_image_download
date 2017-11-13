# -*- coding: UTF-8 -*-

import requests
import re
import sys
import os
from bs4 import BeautifulSoup
import time
import random
import threading


class DownloadTool(object):
    HEADER_POOL = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

    def __init__(self):
        super(DownloadTool, self).__init__()

    @staticmethod
    def get_random_headers():
        header = {'User-Agent': random.choice(DownloadTool.HEADER_POOL)}
        print header
        return header


class Avmoo(object):
    SPLIT_CHAR = '|'
    IMG_PATH = 'img/'

    # HEADERS = {
    # 'User-agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'}

    def __init__(self, porn_star_url, porn_star_name):
        super(Avmoo, self).__init__()
        self.__porn_star_name = porn_star_name
        self.__porn_star_url = porn_star_url
        self.__search_page_file_name = '{}_search.txt'.format(porn_star_name)
        self.__av_list_file_name = '{}_av_list.txt'.format(porn_star_name)
        self.__img_list_file_name = '{}_img_list.txt'.format(porn_star_name)
        self.__img_path = Avmoo.IMG_PATH + porn_star_name + '/'
        if not os.path.exists(self.__img_path):
            os.mkdir(self.__img_path)
        self.__page = 0

    def __call__(self, *args, **kwargs):
        # self.store_search_page_data(2)
        # self.store_search_page_data(3)
        # self.store_search_page_data(4)
        # self.resolve_search_page_data()
        # self.store_all_av_image_url()
        # self.download_all_image()
        self.multi_thread_download_all_image()

    def store_search_page_data(self, page):
        if page == 1:
            url = self.__porn_star_url
        else:
            url = '{}/page/{}'.format(self.__porn_star_url, page)
        page_request = requests.get(url, headers=DownloadTool.get_random_headers(), timeout=30)
        page_request.encoding = 'GBK'
        page_text = page_request.content
        temp = open(self.__search_page_file_name, 'a')
        temp.write(page_text)
        temp.flush()
        temp.close()

    def resolve_search_page_data(self):
        if not os.path.exists(self.__search_page_file_name):
            print 'has no this file:', self.__search_page_file_name
            return
        text = open(self.__search_page_file_name, 'r')
        print 'text is', text
        soup = BeautifulSoup(text, 'html.parser', from_encoding='gb18030')
        text.close()
        av_url_list = soup.find_all('a', href=re.compile(r'https://avmo.club/cn/movie/\w*', re.I))
        lines = [av_node.span.text + Avmoo.SPLIT_CHAR + av_node.attrs['href'] + '\n' for av_node in av_url_list]
        print 'len of lines', len(lines)
        file_av_list = open(self.__av_list_file_name, 'a')
        file_av_list.writelines(lines)
        file_av_list.flush()
        file_av_list.close()

    def store_all_av_image_url(self):
        av_list = open(self.__av_list_file_name, 'r')
        for av_info in av_list:
            arr = av_info.split(Avmoo.SPLIT_CHAR)
            print u'开始解析这部AV:  ', arr[0]
            self.store_av_image_url(arr[0], arr[1])

    def store_av_image_url(self, av_name, av_url):
        print u'获取这部AV的所有样例图片地址 ', av_name, av_url
        try:
            page_request = requests.get(av_url, headers=DownloadTool.get_random_headers(), timeout=30)
            page_request.encoding = 'GBK'
            page_text = page_request.content
        except:
            print u'这一部解析失败', av_name, av_url
            time.sleep(1.0)
            return
        # temp = open('aaa.txt', 'w')
        # temp.write(page_text)
        # temp.flush()
        # temp.close()
        # page_text = open('aaa.txt', 'r')
        soup = BeautifulSoup(page_text, 'html.parser', from_encoding='gb18030')
        # page_text.close()
        stars = soup.find_all('a', class_='avatar-box')
        if len(stars) == 1:
            print u'是单体片，开始解析'
            sample_img_list = soup.find_all('a', class_='sample-box')
            sample_url_list = [sample_node.attrs['href'] + '\n' for sample_node in sample_img_list]
            file_img_list = open(self.__img_list_file_name, 'a')
            file_img_list.writelines(sample_url_list)
            file_img_list.flush()
            file_img_list.close()
        else:
            print u'不是单体片'

    def download_all_image(self):
        print u'开始下载所有图片'
        file_img_list = open(self.__img_list_file_name, 'r')
        image_url_list = file_img_list.readlines()
        self.download_image(image_url_list)

    def download_image(self, image_url_list, thread_num=0):
        for img_url in image_url_list:
            img_url = img_url.strip()
            left = img_url.rfind('/') + 1
            img_path = self.__img_path + img_url[left:]
            if not os.path.exists(img_path):
                print u'开始下载图片, thread_num : ', thread_num, '   img_url', img_url

                try:
                    r = requests.get(img_url, headers=DownloadTool.get_random_headers(), timeout=30)
                    if r and r.content:
                        with open(img_path, 'wb') as img_file:
                            img_file.write(r.content)
                            img_file.close()
                            time.sleep(1.0)
                    else:
                        print u'这也是下载失败了吗'
                except:
                    print u'下载图片失败 thread_num', thread_num

            else:
                print u'图片文件已存在 thread_num', thread_num, '  img_url', img_url

    def multi_thread_download_all_image(self):
        print u'多线程下载图片'
        file_img_list = open(self.__img_list_file_name, 'r')
        lines = file_img_list.readlines()
        threads = []
        for i in range(0, len(lines), 100):
            image_list = lines[i:i + 100]
            t = threading.Thread(target=self.download_image, args=(image_list, i))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


if __name__ == '__main__':
    reload(sys)
    # this is actually useful
    sys.setdefaultencoding('utf-8')
    moo = Avmoo('https://avmo.club/cn/search/%E4%B8%83%E8%8D%89%E3%81%A1%E3%81%A8%E3%81%9B', 'qicao')
    moo(*sys.argv)
    # 1528
    # 1555
    # 1566
