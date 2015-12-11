from multiprocessing import Process
from multiprocessing import Pool

import scipy
import random


def workerFunction(arg):
    scipy.random.seed()
    print arg
    a = [] 
    for i in xrange(10):
        a.append(random.randint(0,20))
    print a



if __name__ == '__main__':
    p = Pool(5)
    a = 'a'
    b = 'b'
    p.map(workerFunction, [(a,b),(a,b),(a,b),(a,b),(a,b),(a,b),(a,b),(a,b),(a,b),(a,b),(a,b),(a,b)])

    # p = Process(target=workerFunction, args=('a','b'))
    # r = Process(target=workerFunction, args=('a','b'))
    # s = Process(target=workerFunction, args=('a','b'))
    # r.start()
    # p.start()
    # s.start()
    # p.join()
    # r.join()
    # s.join()
