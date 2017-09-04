import re
import time
import traceback
import requests


from bs4 import BeautifulSoup
from collections import namedtuple
from souche_crawler.logger import logger
from souche_crawler import constants as C
from souche_crawler.helpers import parse_field
from souche_crawler.models import Car, session, Base, engine

CarItem = namedtuple('CarItem', ['name', 'link'])


class CarBase(object):

    def __init__(self, queue):
        self.queue = queue
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': C.USER_AGENT})

    @staticmethod
    def parse(bs_obj):
        pass

    def fetch(self, url):
        res = self.session.get(url)
        if res.status_code > 200:
            logger.info('Fetch Error, Status Code {}, Will retry'.format(
                res.status_code, url))
            return self.fetch(url)
        logger.info('Fetch {}'.format(url))
        bs_obj = BeautifulSoup(res.text, 'lxml')
        return self.parse(bs_obj)


class CarList(CarBase):

    def __init__(self, queue):
        super(CarList, self).__init__(queue)
        self.max_page = None

    @staticmethod
    def parse(bs_obj):
        titles = [re.sub('[\r\n\t ]+', '', item.text)
                  for item in bs_obj.find_all('a', {'class': 'car-link'})]
        links = [C.SITE_URL + item.attrs.get('href') for item in bs_obj.find_all(
            'a', {'class': 'car-link'})]
        return list(zip(titles, links))

    def init_max_page(self):
        res = self.session.get(C.LIST_URL.format(1))
        bs_obj = BeautifulSoup(res.text, 'lxml')
        self.max_page = int(bs_obj.find(
            'div', {'class': 'sort clearfix'}).find_all('a')[-2].text)

    def run(self):
        self.init_max_page()
        for page in range(1, self.max_page + 1):
            logger.info('Fetch {} Page'.format(page))
            for item in self.fetch(C.LIST_URL.format(page)):
                car = CarItem(*item)
                self.queue.put(car)
                logger.info('Put {}'.format(car))
        self.queue.put('finished')


class CarDetail(CarBase):

    def __init__(self, queue):
        super(CarDetail, self).__init__(queue)

    @staticmethod
    def parse(bs_obj):
        if '本车为全新车' in bs_obj.text:
            return dict(name=bs_obj.ins.text, price=bs_obj.em.text)

        titles = ['name', 'price', 'first_register',
                  'driver_mile', 'location', 'emission_standard', 'contact', 'car_id']
        detail_items = [item.strong.text for item in bs_obj.find(
            'div', {'class': 'car_detail clearfix'}).find_all('div')]
        detail_items.append(bs_obj.find(
            'div', {'class': 'phone-num'}).attrs['data-phonenum'])
        detail_items.append(bs_obj.find(
            'input', {'name': 'carId'}).attrs['value'])

        data = dict(
            zip(titles, [bs_obj.ins.text, bs_obj.em.text] + detail_items))
        return parse_field(data)

    def process(self, url):
        item = self.fetch(url)
        c = Car(**item)
        logger.info('Commit {}'.format(c))
        session.add(c)
        session.commit()

    def run(self):
        Base.metadata.create_all(engine)
        while True:
            try:
                item = self.queue.get()
                if item == 'finished':
                    break
                self.process(item.link)
            except Exception:
                logger.warning(traceback.format_exc())
