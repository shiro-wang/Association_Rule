import ast
from itertools import combinations

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
    # Turn string into a list
    if isinstance(transactions[0], str):
        for tran_count in range(len(transactions)):
            transactions[tran_count] = ast.literal_eval(transactions[tran_count])
    # print(transactions)
    
    # Get all items num from past_lk
    item_exist = []
    item_count = {}
    for old_pattern in transactions:
        for item in old_pattern:
            if item not in item_exist:
                item_exist.append(item)
                item_count[item] = 1
            else:
                item_count[item] += 1
    # print("Before")
    # print(item_exist)
    # print(item_count)
    # 第一步篩選：若要組(0,1,2)則(0,1),(1,2),(0,2)都要在past_lk，意思是多的item至少出現2次(now_k)
    delete_items = []
    for item in item_exist:
        if item_count[item] < now_k:
            delete_items.append(item)
            
    # print("After")
    # print(delete_items)
    for del_item in delete_items:
        item_exist.remove(del_item)
        item_count.pop(del_item)
    item_exist = sorted(item_exist)
    # print(item_exist)
    # print(dict(sorted(item_count.items())))
    
    # print(item_count)
    # Method 1
    # catch_pattern = []
    # for antecedent_id in range(len(transactions)-1):
    #     for consequent_id in range(antecedent_id+1, len(transactions)):
    #         combined_set = list(transactions[antecedent_id])
    #         combined_set += list(transactions[consequent_id])
    #         combined_set = set(combined_set)
    #         combined_set = list(combined_set)
            
    #         # 個數篩選
    #         if len(combined_set) == now_k+1:
    #             # 通過個數篩選下來的pattern先存放，避免重複計算
    #             in_catch = False
    #             for c_pt in catch_pattern:
    #                 if all(elem in c_pt for elem in combined_set):
    #                     in_catch = True
    #                     break
    #             if in_catch == False:
    #                 catch_pattern.append(combined_set)
    #                 # print(combined_set)
    #                 # 計算此pattern個數
    #                 pattern_count = 0
    #                 for tran in dataset:
    #                     if all(elem in tran  for elem in combined_set):
    #                         pattern_count += 1
    #                 if pattern_count >= min_sup_num:
    #                     new_lk[str(combined_set)] = pattern_count
    # print(dict(list(new_lk.items())[:5]))
    # print(len(new_lk))
    
    # Method 2
    for old_pattern in transactions:
        # print(old_pattern)
        
        # 取此pattern最大值，確保往後不會有重複
        biggest_item = old_pattern[-1]
        if biggest_item in item_exist:
            biggest_item_pos = item_exist.index(biggest_item)
            for new_item_pos in range(biggest_item_pos+1, len(item_exist)):
                combined_set = old_pattern.copy()
                combined_set.append(str(item_exist[new_item_pos]))
                # print(combined_set)
                
                # 計算此pattern個數
                pattern_count = 0
                for tran in dataset:
                    if all(elem in tran for elem in combined_set):
                        pattern_count += 1
                if pattern_count >= min_sup_num:
                    new_lk[str(combined_set)] = pattern_count
    print(dict(list(new_lk.items())[:5]))
    
    # test
    # new_lk.update(past_lk)
    # return new_lk
    
    if len(new_lk) == 0:
        return new_lk
    # We can't use "return dict.update()" because the original dictionary doesn't contain any keys
    new_lk.update(create_itemset_lk(dataset, new_lk, min_sup_num))
    return new_lk

# output: [antecedent,consequent,support,confidence,lift]
def get_apriori_results(dataset, l1, all_lk):
    # 先複製一份出來
    pre_process = {}
    pre_process.update(all_lk)
    all_lk.update(l1)
    outputs = []
    # 取結果出來
    for freq_pat, sup in pre_process.items():
        # str轉python
        freq_pat = ast.literal_eval(freq_pat)
        # print(freq_pat)
        # 可能的所有組合
        for k in range(1, len(freq_pat)):
            candidates = list(combinations(freq_pat, k))
            # print(candidates)
            # [(0,), (1,),]
            processed_candidates = []
            for cand in candidates:
                # (0,)
                untuple_cand = []
                for c in cand:
                    untuple_cand.append(c)
                processed_candidates.append(untuple_cand)
            # print(processed_candidates)
            
            # [['0'], ['1']]
            for cand_list in processed_candidates:
                consequent = []
                for elem in freq_pat:
                    if elem not in cand_list:
                        consequent.append(elem)
                cand_list = str(cand_list)
                
                antecedent = cand_list
                consequent = str(consequent)
                # print(cand_list)
                # print(consequent)
                # print(all_lk[antecedent])
                support = sup / len(dataset)
                confidence = sup / all_lk[antecedent]
                lift = sup / all_lk[antecedent] / all_lk[consequent] * len(dataset)
                outputs.append([ast.literal_eval(antecedent), ast.literal_eval(consequent), support, confidence, lift])
    return outputs

def do_apriori(dataset, min_sup_num):
    l1 = create_itemset_l1(dataset, min_sup_num)
    # print(l1)
    all_lk = create_itemset_lk(dataset, l1, min_sup_num)
    print('After remove single apriori: ', len(all_lk))
    results = get_apriori_results(dataset, l1, all_lk)
    # print(results)
    # print(l1)
    return results