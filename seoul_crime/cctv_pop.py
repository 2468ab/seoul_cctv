import numpy as np
import pandas as pd
from seoul_crime.data_reader import DataReader


# cctv = '기관명', '소계', '2013년도 이전', '2014년', '2015년', '2016년'
# pop = '자치구', '계', '계.1', '계.2', '65세이상고령자'

class CCTVModel:
    def __init__(self):
        self.dr = DataReader()

    def hook_process(self):
        print('--------- 1. CCTV 파일 DF 생성 -------------')
        self.get_cctv()

    def get_cctv(self):
        self.dr.context = './data/'
        self.dr.fname = 'cctv_in_seoul.csv'
        cctv = self.dr.csv_to_dframe()
        self.dr.fname = 'pop_in_seoul.xls'
        pop = self.dr.xls_to_dframe(2,'B,D,G,J,N')
        print(cctv.columns)
        print(pop.columns)