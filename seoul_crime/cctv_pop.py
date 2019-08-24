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
        cctv.rename(columns={cctv.columns[0]: '구별'}, inplace=True)
        pop.rename(columns={
            pop.columns[0]: '구별',
            pop.columns[1]: '인구수',
            pop.columns[2]: '한국인',
            pop.columns[3]: '외국인',
            pop.columns[4]: '고령자',
        }, inplace=True)
        #pop.drop([0],axis=0)
        pop.drop([26], inplace=True)
        pop['외국인비율'] = pop['외국인'] / pop['인구수'] * 100
        pop['고령자비율'] = pop['고령자'] / pop['인구수'] * 100

        cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], 1, inplace=True)
        cctv_pop = pd.merge(cctv, pop, on='구별')
        cor1 = np.corrcoef(cctv_pop['고령자비율'], cctv_pop['소계'])
        cor2 = np.corrcoef(cctv_pop['외국인비율'], cctv_pop['소계'])
        print(cor1, '고령자,CCTV')
        print(cor2, '외국인,CCTV')

        cctv_pop.to_csv('./saved_data/cctv_pop.csv')

        """
        [[ 1.         -0.28078554]
        [-0.28078554  1.        ]] 고령자,CCTV
        [[ 1.         -0.13607433]
        [-0.13607433  1.        ]] 외국인,CCTV
        """
