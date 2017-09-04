from souche_crawler.core import CarList, CarDetail
from souche_crawler.models import *
from queue import Queue


from threading import Thread


q = Queue()
t1 = Thread(target=CarList(q).run)
t2 = Thread(target=CarDetail(q).run)

t1.start()
t2.start()
t1.join()
t2.join(timeout=None)
