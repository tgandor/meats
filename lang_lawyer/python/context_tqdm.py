#!/usr/bin/env python3

# https://stackoverflow.com/a/41921948/1338797

from multiprocessing import Pool
import time
from tqdm import *

def _foo(my_number):
   square = my_number * my_number
   time.sleep(1)
   return square 

if __name__ == '__main__':
    print('With inner tqdm')
    max_ = 15
    with Pool(processes=2) as p:
        with tqdm(total=max_) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(_foo, range(0, max_)))):
                pbar.update()
    print('Without inner tqdm')
    max_ = 15
    with Pool(processes=2) as p:
        with tqdm(total=max_) as pbar:
            for i, _ in enumerate(p.imap_unordered(_foo, range(0, max_))):
                pbar.update()

