import numpy as np
import pandas as pd
import ast
from data_proc import turn_to_list
# output: ['antecedent', 'consequent', 'lift', 'confidence', 'support']

def create_itemset_l1(dataset, min_sup_num):
    l1 = {}
    for transaction in dataset:
        for item in transaction:
            if item not in l1:
                l1[item] = 1
            else:
                l1[item] += 1   
    delete_item = []
    for item, value in l1.items():
        if value < min_sup_num:
            delete_item.append(item)
    for delete in delete_item:
        del l1[delete]
    return l1
    
def create_itemset_lk(dataset, lk, min_sup_num):
    if isinstance(next(iter(lk)), int):
        now_k = len(next(iter(lk)))
    else:
        now_k = len(ast.literal_eval(next(iter(lk))))
    # print(now_k)
    transactions = list(lk.keys())
    if isinstance(transactions[0], str):
        for tran_count in range(len(transactions)):
            transactions[tran_count] = ast.literal_eval(transactions[tran_count])
    # print(list([transactions[3]]))
    lk = {}
    for antecedent_id in range(0,len(transactions)-1):
        for consequent_id in range(antecedent_id+1, len(transactions)):
            combined_set = []
            combined_set = list([transactions[antecedent_id]])
            combined_set += list([transactions[consequent_id]])
            combined_set = set(combined_set)
            combined_set = list(combined_set)
            if len(combined_set) == now_k+1:
                pattern_count = 0
                for tran in dataset:
                    if all(elem in tran  for elem in combined_set):
                        pattern_count += 1
                if pattern_count >= min_sup_num:
                    lk[str(combined_set)] = pattern_count
        break
    # print(lk)
    return lk.update(create_itemset_lk(dataset, lk, min_sup_num))
    
def apriori(input_data, a):
    dataset = turn_to_list(input_data)
    min_sup_num = a.min_sup*len(dataset)

    l1 = create_itemset_l1(dataset, min_sup_num)
    all_lk = create_itemset_lk(dataset, l1, min_sup_num)
    print(all_lk)
    # print(l1)
    # return results
