import ast
from itertools import combinations

class FP_treeNode:
    def __init__(self, itemname, count, parrentNode):
        self.itemname = itemname
        self.count = count
        self.parrentNode = parrentNode
        self.nodeLink = None
        self.children = {}
        
    def increase(self, occurrences):
        self.count += occurrences
        
    def display(self, ind=0):
        print(f"{' '*ind} {self.itemname} {self.count}")
        for child in self.children.values():
            child.display(ind+1)

# Update header linklist
def update_Header(node, target_node):
    while node.nodeLink is not None:
        node = node.nodeLink
    node.nodeLink = target_node

# Update FP_tree，包含更新header_table
def update_FPtree(items, now_Node, header_table, count):
    if items[0] in now_Node.children:
        # 判斷是否已存在於子結點，有的話子count+1
        now_Node.children[items[0]].increase(count)
    else:
        # 創建新的分支
        now_Node.children[items[0]] = FP_treeNode(items[0], count, now_Node)
        # 更新header linklist
        if header_table[items[0]][1] == None:
            header_table[items[0]][1] = now_Node.children[items[0]]
        else:
            update_Header(header_table[items[0]][1], now_Node.children[items[0]])
    
    # 遞迴往下
    if len(items) > 1:
        update_FPtree(items[1::], now_Node.children[items[0]], header_table, count)

def create_itemset_newdata(dataset, min_sup_num):
    '''
    :return: new_dataset: 新的transaction list, 去掉低於min_sup, 經過item_count排序
    :return: item_head: [("['38']", 2265), ("['36']", 1879),...]
    '''
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
        for tran in dataset:
            if delete in tran:
                tran.remove(delete)
    # 各項目依照次數排序
    item_head = sorted(l1.items(), key=lambda x: x[1], reverse=True)
    # print(item_head)
    # [("['38']", 2265), ("['36']", 1879),...]
    new_dataset = []
    # transaction 內元素依照次數sort排序
    for transaction in dataset:
        new_data = []
        for item, value in item_head:
            # print(item, value)
            if item in transaction:
                new_data.append(item)
        new_dataset.append(new_data)
    # print(new_dataset)
    
    return new_dataset, item_head

# 回朔找prefix pattern
def ascendFPtree(leafNode, prefixPath):
    if leafNode.parrentNode != None:
        prefixPath.append(leafNode.itemname)
        ascendFPtree(leafNode.parrentNode, prefixPath)

# 輸入節點，找prefix_path後形成condition pattern     
def find_prefix_path(base_pattern, header_table):
    '''
    :param base_pattern: 要查詢的pat
    :param header_table: 查詢nodetree中pattern所在節點 透過header_table linklist一個個找
    :return: cond_pat 建構condition pattern base要用到的cond_pat
    '''
    condition_pat = {}
    treeNode = header_table[base_pattern][1]
    # 照header_table linklist循環找prefix
    while treeNode != None:
        prefix_path = []
        ascendFPtree(treeNode, prefix_path)
        # 去掉最基本的Null Set頭
        if len(prefix_path) > 1:
            condition_pat[frozenset(prefix_path[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condition_pat

def mineFPtree(FP_tree, header_table, min_sup_num, pre_freq_set, freq_patterns):
    # 從小到大得到item
    # print(header_table)
    itemsL = [v[0] for v in sorted(header_table.items(), key=lambda x: x[1][0])]
    # print('itmesL= ', itemsL)
    for base_pattern in itemsL:
        new_freq_set = pre_freq_set.copy()
        new_freq_set.add(base_pattern)
        # print('new_freq_set=', new_freq_set, pre_freq_set)
        # print(header_table[base_pattern][1].count)
        freq_patterns[str(new_freq_set)] = header_table[base_pattern][1].count
        # print('freq_patterns=', freq_patterns)
        condpat_bases = find_prefix_path(base_pattern, header_table)
        cond_tree, cond_head = create_FPtree_bydict(condpat_bases, min_sup_num)
        
        if cond_head != None:
            # cond_tree.display()
            mineFPtree(cond_tree, cond_head, min_sup_num, new_freq_set, freq_patterns)
    
def create_FPtree_bydict(dataset, min_sup_num):
    # print(dataset)
    header_table = {}
    for trans in dataset:
        for item in trans:
            header_table[item] = header_table.get(item, 0) + dataset[trans]
    delete_k = []
    for k in header_table.keys():
        if header_table[k] < min_sup_num:
            delete_k.append(k)
    for k in delete_k:
        del(header_table[k])
    # print(header_table)
    freq_item_set = set(header_table.keys())
    if len(freq_item_set) == 0:
        return None, None
    
    new_header_table = {}
    for k,v in header_table.items():
        new_header_table[k] = [v, None]
    header_table = new_header_table
    # print(header_table)
    return_tree = FP_treeNode('Null Set',1,None)
    for tran_set, count in dataset.items():
        # 紀錄階段性item出現次數
        localD = {}
        for item in tran_set:
            if item in freq_item_set:
                # print('header_table[item][0]=', header_table[item][0], header_table[item])
                localD[item] = header_table[item][0]
        if len(localD)> 0:
            ordered_item = [v[0] for v in sorted(localD.items(), key=lambda p:(p[1], (p[0])), reverse=True)]
            update_FPtree(ordered_item, return_tree, header_table, count)
    return return_tree, header_table

def get_fpgrwoth_results(dataset, freq_patterns):
    
    outputs = []
    # 取結果出來
    for freq_pat, sup in freq_patterns.items():
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
                confidence = sup / freq_patterns[antecedent]
                lift = sup / freq_patterns[antecedent] / freq_patterns[consequent] * len(dataset)
                outputs.append([ast.literal_eval(antecedent), ast.literal_eval(consequent), support, confidence, lift])
    return outputs
# main function
def do_fp_growth(dataset, min_sup_num):
    # dataset = [['m','br','be'],
    #            ['br','c'],
    #            ['br','e'],
    #            ['m','br','c'],
    #            ['m','e'],
    #            ['br','e'],
    #            ['m','e'],
    #            ['m','br','e','be'],
    #            ['m','br','e']]
    # min_sup_num = 2
    
    new_dataset, item_head = create_itemset_newdata(dataset, min_sup_num)
    
    header_table = {}
    for item in item_head:
        header_table[item[0]] = [item[1], None] # [count, node]
    # print(header_table)
    FP_tree = FP_treeNode('Null Set', 1, None)
    for ordered_transaction in new_dataset:
        update_FPtree(ordered_transaction, FP_tree, header_table, 1)
    # FP_tree.display()
    # print(find_prefix_path('be', header_table))
    freq_patterns = {}
    mineFPtree(FP_tree, header_table, min_sup_num, set([]), freq_patterns)
    
    # print('Before remove single fp_growth: ', len(freq_patterns))
    
    delete_single_pattern = []
    for k,v in freq_patterns.items():
        if len(ast.literal_eval(k)) == 1:
            delete_single_pattern.append(k)
    for d in delete_single_pattern:
        freq_patterns.pop(d)
    print('After remove single fp_growth: ', len(freq_patterns))
    # for k,v in freq_patterns.items():  
    #     print(k,v)
    results = get_fpgrwoth_results(dataset, freq_patterns)
    return {}