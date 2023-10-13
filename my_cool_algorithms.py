import numpy as np
import pandas as pd
import ast
from itertools import combinations
from utils import turn_to_list, timer
from Apriori import do_apriori
from FP_growth import do_fp_growth

@timer 
def apriori(input_data, a):
    dataset = turn_to_list(input_data)
    min_sup_num = a.min_sup*len(dataset)
    # print(len(dataset))
    # print(min_sup_num)
    results = do_apriori(dataset, min_sup_num)
    
    return results

@timer
def fp_growth(input_data, a):
    dataset = turn_to_list(input_data)
    min_sup_num = a.min_sup*len(dataset)
    # print(len(dataset))
    # print(min_sup_num)
    results = do_fp_growth(dataset, min_sup_num)
    
    return results