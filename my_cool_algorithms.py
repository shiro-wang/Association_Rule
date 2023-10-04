import numpy as np
import pandas as pd
import ast
from utils import turn_to_list, timer

# output: ['antecedent', 'consequent', 'lift', 'confidence', 'support']

def create_itemset_l1(dataset, min_sup_num):
    l1 = {}
    for transaction in dataset:
        for item in transaction:
            if str([item]) not in l1:
                l1[str([item])] = 1
            else:
                l1[str([item])] += 1   
    delete_item = []
    for item, value in l1.items():
        if value < min_sup_num:
            delete_item.append(item)
    for delete in delete_item:
        del l1[delete]
    return l1
    
def create_itemset_lk(dataset, past_lk, min_sup_num):
    now_k = len(ast.literal_eval(next(iter(past_lk))))
    print(now_k)
    transactions = list(past_lk.keys())
    
    new_lk = {}
    combined_set = []
    if isinstance(transactions[0], str):
        for tran_count in range(len(transactions)):
            transactions[tran_count] = ast.literal_eval(transactions[tran_count])
    # print(transactions)
    catch_pattern = []
    for antecedent_id in range(len(transactions)-1):
        for consequent_id in range(antecedent_id+1, len(transactions)):
            combined_set = list(transactions[antecedent_id])
            combined_set += list(transactions[consequent_id])
            combined_set = set(combined_set)
            combined_set = list(combined_set)
            
            # 個數篩選
            if len(combined_set) == now_k+1:
                # 通過個數篩選下來的pattern先存放，避免重複計算
                in_catch = False
                for c_pt in catch_pattern:
                    if all(elem in c_pt for elem in combined_set):
                        in_catch = True
                        break
                if in_catch == False:
                    catch_pattern.append(combined_set)
                    # print(combined_set)
                    # 計算此pattern個數
                    pattern_count = 0
                    for tran in dataset:
                        if all(elem in tran  for elem in combined_set):
                            pattern_count += 1
                    if pattern_count >= min_sup_num:
                        new_lk[str(combined_set)] = pattern_count
    print(dict(list(new_lk.items())[:5]))
    print(len(new_lk))
    if len(new_lk) == 0:
        return new_lk
    # We can't use "return dict.update()" because the original dictionary doesn't contain any keys and
    new_lk.update(create_itemset_lk(dataset, new_lk, min_sup_num))
    return new_lk

@timer 
def apriori(input_data, a):
    dataset = turn_to_list(input_data)
    min_sup_num = a.min_sup*len(dataset)
    # print(len(dataset))
    # print(min_sup_num)

    l1 = create_itemset_l1(dataset, min_sup_num)
    # print(l1)
    all_lk = create_itemset_lk(dataset, l1, min_sup_num)
    print(len(all_lk))
    # print(l1)
    
    # return results
